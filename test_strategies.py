#!/usr/bin/env python3
"""
简单测试脚本，验证两种期权策略的筛选功能
"""

import sys
import pandas as pd
from option_screener_gui import (
    get_stock_data, 
    find_potential_expirations,
    analyze_and_filter_puts,
    analyze_and_filter_calls
)

def test_strategies():
    """测试两种期权策略"""
    
    # 测试参数
    ticker = "AAPL"
    min_dte = 30
    max_dte = 45
    min_otm = 0.05
    max_otm = 0.15
    
    print(f"🧪 测试股票: {ticker}")
    print(f"📅 到期天数范围: {min_dte}-{max_dte}天")
    print(f"📊 价外范围: {min_otm*100:.1f}%-{max_otm*100:.1f}%")
    print("-" * 50)
    
    # 获取股票数据
    try:
        stock, current_price = get_stock_data(ticker)
        if stock is None:
            print("❌ 无法获取股票数据")
            return
            
        print(f"💰 当前价格: ${current_price:.2f}")
        
        # 查找到期日
        expirations = find_potential_expirations(stock, min_dte, max_dte)
        if not expirations:
            print("❌ 未找到符合条件的到期日")
            return
            
        print(f"📅 找到 {len(expirations)} 个到期日")
        
        # 测试第一个到期日
        exp, dte = expirations[0]
        print(f"🎯 测试到期日: {exp} ({dte}天)")
        
        # 测试看跌期权
        print("\n📉 测试现金担保看跌期权:")
        puts_df = analyze_and_filter_puts(stock, exp, dte, current_price, min_otm, max_otm)
        if not puts_df.empty:
            print(f"✅ 找到 {len(puts_df)} 个看跌期权机会")
            best_put = puts_df.iloc[0]
            print(f"   最佳机会: 行权价${best_put['strike']:.2f}, 年化收益率{best_put['annualizedReturn']:.2%}")
        else:
            print("❌ 未找到看跌期权机会")
        
        # 测试看涨期权
        print("\n📈 测试备兑看涨期权:")
        calls_df = analyze_and_filter_calls(stock, exp, dte, current_price, min_otm, max_otm)
        if not calls_df.empty:
            print(f"✅ 找到 {len(calls_df)} 个看涨期权机会")
            best_call = calls_df.iloc[0]
            print(f"   最佳机会: 行权价${best_call['strike']:.2f}, 年化收益率{best_call['annualizedReturn']:.2%}")
        else:
            print("❌ 未找到看涨期权机会")
            
        print("\n🎉 测试完成!")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")

if __name__ == "__main__":
    test_strategies()