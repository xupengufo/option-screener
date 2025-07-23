import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="期权筛选器",
    page_icon="📈",
    layout="wide"
)

# Default values
DEFAULT_TICKER = 'DPST'
DEFAULT_DAYS_TO_EXPIRATION_MIN = 30
DEFAULT_DAYS_TO_EXPIRATION_MAX = 45
DEFAULT_OTM_PERCENTAGE_MIN = 0.05
DEFAULT_OTM_PERCENTAGE_MAX = 0.15

@st.cache_data(ttl=300)  # 缓存5分钟
def get_stock_data(ticker_symbol):
    """获取股票数据和当前价格"""
    try:
        stock = yf.Ticker(ticker_symbol)
        
        # 尝试多种方式获取当前价格
        current_price = None
        
        # 方法1: 从info获取
        try:
            current_price = stock.info.get('regularMarketPrice')
        except:
            pass
            
        # 方法2: 从历史数据获取
        if current_price is None or pd.isna(current_price):
            try:
                hist = stock.history(period='1d')
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
            except:
                pass
        
        # 方法3: 从快速信息获取
        if current_price is None or pd.isna(current_price):
            try:
                fast_info = stock.fast_info
                current_price = fast_info.last_price
            except:
                pass

        if current_price is None or pd.isna(current_price):
            raise ValueError(f"无法获取 {ticker_symbol} 的有效价格")
            
        return stock, float(current_price)
    except Exception as e:
        st.error(f"获取股票数据时出错: {e}")
        st.info("💡 提示：请检查股票代码是否正确，或稍后重试")
        return None, None

def find_potential_expirations(stock, min_dte, max_dte):
    """查找指定DTE范围内的到期日"""
    today = date.today()
    potential_expirations = []
    for exp_str in stock.options:
        exp_date = date.fromisoformat(exp_str)
        dte = (exp_date - today).days
        if min_dte <= dte <= max_dte:
            potential_expirations.append((exp_str, dte))
    return potential_expirations

def analyze_and_filter_puts(stock, exp, dte, current_price, min_otm, max_otm):
    """分析和筛选看跌期权"""
    try:
        puts = stock.option_chain(exp).puts

        # 按OTM范围筛选
        min_strike = current_price * (1 - max_otm)
        max_strike = current_price * (1 - min_otm)
        
        filtered_puts = puts[
            (puts['strike'] >= min_strike) &
            (puts['strike'] <= max_strike)
        ].copy()

        # 使用bid价格，如果为0则使用lastPrice
        filtered_puts['premium'] = filtered_puts.apply(
            lambda row: row['bid'] if row['bid'] > 0 else row['lastPrice'], axis=1
        )
        
        # 筛选有价格数据的期权
        filtered_puts = filtered_puts[filtered_puts['premium'] > 0]
        
        # 计算抵押品
        filtered_puts['collateral'] = filtered_puts['strike'] * 100
        filtered_puts = filtered_puts[filtered_puts['collateral'] > 0]

        if filtered_puts.empty:
            return pd.DataFrame()

        # 计算年化收益率
        filtered_puts['annualizedReturn'] = (
            (filtered_puts['premium'] * 100) / filtered_puts['collateral']
        ) * (365 / dte)
        
        filtered_puts['dte'] = dte
        
        # 计算近似delta
        filtered_puts['approx_delta'] = abs(filtered_puts['strike'] - current_price) / current_price
        
        return filtered_puts
    except Exception as e:
        st.error(f"分析期权数据时出错: {e}")
        return pd.DataFrame()

def analyze_and_filter_calls(stock, exp, dte, current_price, min_otm, max_otm):
    """分析和筛选看涨期权"""
    try:
        calls = stock.option_chain(exp).calls

        # 按OTM范围筛选 (对于看涨期权，OTM意味着行权价高于当前价格)
        min_strike = current_price * (1 + min_otm)
        max_strike = current_price * (1 + max_otm)
        
        filtered_calls = calls[
            (calls['strike'] >= min_strike) &
            (calls['strike'] <= max_strike)
        ].copy()

        # 使用bid价格，如果为0则使用lastPrice
        filtered_calls['premium'] = filtered_calls.apply(
            lambda row: row['bid'] if row['bid'] > 0 else row['lastPrice'], axis=1
        )
        
        # 筛选有价格数据的期权
        filtered_calls = filtered_calls[filtered_calls['premium'] > 0]
        
        # 对于备兑看涨期权，抵押品是股票本身（100股）
        filtered_calls['collateral'] = current_price * 100
        filtered_calls = filtered_calls[filtered_calls['collateral'] > 0]

        if filtered_calls.empty:
            return pd.DataFrame()

        # 计算年化收益率
        filtered_calls['annualizedReturn'] = (
            (filtered_calls['premium'] * 100) / filtered_calls['collateral']
        ) * (365 / dte)
        
        filtered_calls['dte'] = dte
        
        # 计算近似delta
        filtered_calls['approx_delta'] = abs(filtered_calls['strike'] - current_price) / current_price
        
        return filtered_calls
    except Exception as e:
        st.error(f"分析期权数据时出错: {e}")
        return pd.DataFrame()

def screen_options_gui(ticker, min_dte, max_dte, min_otm, max_otm, strategy_type):
    """GUI版本的期权筛选主函数"""
    
    # 获取股票数据
    with st.spinner(f'正在获取 {ticker.upper()} 的数据...'):
        stock, current_price = get_stock_data(ticker)
        
    if stock is None or current_price is None:
        return None, None
    
    # 查找到期日
    expirations = find_potential_expirations(stock, min_dte, max_dte)
    if not expirations:
        st.warning(f"在 {min_dte}-{max_dte} 天到期窗口内未找到期权")
        return None, current_price

    # 分析所有到期日的期权
    all_opportunities = []
    progress_bar = st.progress(0)
    
    for i, (exp, dte) in enumerate(expirations):
        if strategy_type == "现金担保看跌期权":
            opportunities = analyze_and_filter_puts(
                stock, exp, dte, current_price, min_otm, max_otm
            )
        else:  # 备兑看涨期权
            opportunities = analyze_and_filter_calls(
                stock, exp, dte, current_price, min_otm, max_otm
            )
            
        if not opportunities.empty:
            all_opportunities.append(opportunities)
        progress_bar.progress((i + 1) / len(expirations))

    if not all_opportunities:
        return pd.DataFrame(), current_price
    else:
        result_df = pd.concat(all_opportunities)
        result_df = result_df.sort_values('annualizedReturn', ascending=False)
        return result_df, current_price

# Streamlit 界面
def main():
    st.title("📈 期权策略筛选器")
    st.markdown("---")
    
    # 侧边栏参数设置
    st.sidebar.header("📊 筛选参数")
    
    # 策略选择
    strategy_type = st.sidebar.selectbox(
        "选择期权策略",
        ["现金担保看跌期权", "备兑看涨期权"],
        help="选择要筛选的期权策略类型"
    )
    
    ticker = st.sidebar.text_input(
        "股票代码", 
        value=DEFAULT_TICKER,
        help="输入要分析的股票代码，如 AAPL, TSLA, DPST"
    ).upper()
    
    st.sidebar.subheader("到期时间范围")
    min_dte = st.sidebar.slider(
        "最小到期天数", 
        min_value=1, 
        max_value=90, 
        value=DEFAULT_DAYS_TO_EXPIRATION_MIN,
        help="期权的最小到期天数"
    )
    
    max_dte = st.sidebar.slider(
        "最大到期天数", 
        min_value=1, 
        max_value=90, 
        value=DEFAULT_DAYS_TO_EXPIRATION_MAX,
        help="期权的最大到期天数"
    )
    
    st.sidebar.subheader("价外程度范围")
    
    # 根据策略类型调整说明文字
    if strategy_type == "现金担保看跌期权":
        otm_help_min = "看跌期权行权价相对当前价格的最小价外百分比（行权价低于当前价格）"
        otm_help_max = "看跌期权行权价相对当前价格的最大价外百分比（行权价低于当前价格）"
    else:
        otm_help_min = "看涨期权行权价相对当前价格的最小价外百分比（行权价高于当前价格）"
        otm_help_max = "看涨期权行权价相对当前价格的最大价外百分比（行权价高于当前价格）"
    
    min_otm = st.sidebar.slider(
        "最小价外百分比", 
        min_value=0.01, 
        max_value=0.30, 
        value=DEFAULT_OTM_PERCENTAGE_MIN,
        format="%.2f",
        help=otm_help_min
    )
    
    max_otm = st.sidebar.slider(
        "最大价外百分比", 
        min_value=0.01, 
        max_value=0.30, 
        value=DEFAULT_OTM_PERCENTAGE_MAX,
        format="%.2f",
        help=otm_help_max
    )
    
    # 主要内容区域
    if st.sidebar.button("🔍 开始筛选", type="primary"):
        if not ticker:
            st.error("请输入股票代码")
            return
            
        if min_dte >= max_dte:
            st.error("最小到期天数必须小于最大到期天数")
            return
            
        if min_otm >= max_otm:
            st.error("最小价外百分比必须小于最大价外百分比")
            return
        
        # 执行筛选
        result_df, current_price = screen_options_gui(ticker, min_dte, max_dte, min_otm, max_otm, strategy_type)
        
        if current_price is None:
            return
            
        # 显示当前价格和策略信息
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("股票代码", ticker)
        with col2:
            st.metric("当前价格", f"${current_price:.2f}")
        with col3:
            st.metric("策略类型", strategy_type)
        with col4:
            if result_df is not None and not result_df.empty:
                st.metric("找到机会", f"{len(result_df)} 个")
            else:
                st.metric("找到机会", "0 个")
        
        st.markdown("---")
        
        # 显示结果
        if result_df is not None and not result_df.empty:
            st.subheader(f"🎯 {strategy_type}筛选结果")
            
            # 准备显示数据
            display_df = result_df[[
                'contractSymbol', 'dte', 'strike', 'premium', 'approx_delta',
                'volume', 'openInterest', 'annualizedReturn'
            ]].copy()
            
            # 格式化数据
            display_df['strike'] = display_df['strike'].map('${:.2f}'.format)
            display_df['premium'] = display_df['premium'].map('${:.2f}'.format)
            display_df['approx_delta'] = display_df['approx_delta'].map('{:.3f}'.format)
            display_df['annualizedReturn'] = display_df['annualizedReturn'].map('{:.2%}'.format)
            
            # 重命名列
            display_df.columns = [
                '合约代码', '到期天数', '行权价', '权利金', '近似Delta',
                '成交量', '持仓量', '年化收益率'
            ]
            
            # 显示表格
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
            # 创建图表
            st.subheader("📊 数据可视化")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 年化收益率图表
                fig1 = px.bar(
                    result_df.head(10), 
                    x='strike', 
                    y='annualizedReturn',
                    title='前10个机会的年化收益率',
                    labels={'strike': '行权价', 'annualizedReturn': '年化收益率'}
                )
                fig1.update_layout(yaxis_tickformat='.2%')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # 到期天数分布
                fig2 = px.histogram(
                    result_df, 
                    x='dte',
                    title='到期天数分布',
                    labels={'dte': '到期天数', 'count': '数量'}
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # 散点图：收益率 vs 风险
            # 处理数据中的 NaN 值和无效数据
            plot_df = result_df.copy()
            
            # 清理数据
            plot_df['volume'] = pd.to_numeric(plot_df['volume'], errors='coerce').fillna(1)
            plot_df['approx_delta'] = pd.to_numeric(plot_df['approx_delta'], errors='coerce')
            plot_df['annualizedReturn'] = pd.to_numeric(plot_df['annualizedReturn'], errors='coerce')
            plot_df['strike'] = pd.to_numeric(plot_df['strike'], errors='coerce')
            plot_df['dte'] = pd.to_numeric(plot_df['dte'], errors='coerce')
            plot_df['premium'] = pd.to_numeric(plot_df['premium'], errors='coerce')
            
            # 移除包含 NaN 的行
            plot_df = plot_df.dropna(subset=['approx_delta', 'annualizedReturn', 'volume'])
            plot_df = plot_df[plot_df['volume'] > 0]  # 只保留volume > 0的数据
            
            if not plot_df.empty and len(plot_df) > 1:
                try:
                    fig3 = px.scatter(
                        plot_df,
                        x='approx_delta',
                        y='annualizedReturn',
                        size='volume',
                        hover_data=['strike', 'dte', 'premium'],
                        title='收益率 vs 风险分析',
                        labels={
                            'approx_delta': '近似Delta (风险指标)',
                            'annualizedReturn': '年化收益率',
                            'volume': '成交量'
                        }
                    )
                    fig3.update_layout(yaxis_tickformat='.2%')
                    st.plotly_chart(fig3, use_container_width=True)
                except Exception as e:
                    st.info(f"散点图生成遇到问题，跳过显示: {str(e)}")
            else:
                st.info("数据不足，无法生成散点图")
            
        else:
            st.warning("未找到符合条件的期权机会，请尝试调整筛选条件")
    
    # 说明信息
    st.markdown("---")
    st.subheader("📖 使用说明")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **策略说明：**
        - **现金担保看跌期权**: 卖出看跌期权，收取权利金，需要现金担保
        - **备兑看涨期权**: 持有股票的同时卖出看涨期权，收取权利金
        
        **参数说明：**
        - **股票代码**: 要分析的股票代码
        - **到期天数**: 期权到期的天数范围
        - **价外百分比**: 期权行权价相对当前价格的价外程度
        """)
    
    with col2:
        st.markdown("""
        **列说明：**
        - **行权价**: 期权的执行价格
        - **权利金**: 期权的卖出价格（每股）
        - **近似Delta**: 与当前价格的距离（越小越接近）
        - **年化收益率**: 如果期权到期无价值的预估收益率
        
        **风险提示：**
        - 现金担保看跌：可能被迫以行权价买入股票
        - 备兑看涨：可能被迫以行权价卖出股票
        """)
    
    # 免责声明
    st.markdown("---")
    st.error("""
    **⚠️ 重要免责声明：**
    
    此工具仅供信息和教育目的使用。期权交易具有固有风险，可能不适合所有投资者。
    提供的数据可能存在延迟或不准确。请务必进行自己的研究(DYOR)。这不是财务建议。
    
    **策略风险：**
    - **现金担保看跌期权**: 如果股价跌破行权价，您需要以行权价购买股票
    - **备兑看涨期权**: 如果股价超过行权价，您的股票可能被以行权价卖出
    """)

if __name__ == "__main__":
    main()