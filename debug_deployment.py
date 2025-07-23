#!/usr/bin/env python3
"""
部署问题诊断脚本
"""

import sys
import os
import subprocess

def check_python_version():
    """检查Python版本"""
    print(f"🐍 Python版本: {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠️  警告: Python版本过低，建议使用3.8+")
    else:
        print("✅ Python版本符合要求")

def check_required_packages():
    """检查必需的包"""
    required_packages = ['streamlit', 'yfinance', 'pandas', 'plotly']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"\n💡 安装缺失的包:")
        print(f"pip install {' '.join(missing_packages)}")
    
    return len(missing_packages) == 0

def check_main_file():
    """检查主文件"""
    if os.path.exists('option_screener_gui.py'):
        print("✅ 主文件 option_screener_gui.py 存在")
        
        # 尝试导入主文件
        try:
            import option_screener_gui
            print("✅ 主文件可以正常导入")
        except Exception as e:
            print(f"❌ 主文件导入失败: {e}")
            return False
    else:
        print("❌ 主文件 option_screener_gui.py 不存在")
        return False
    
    return True

def check_requirements_file():
    """检查requirements.txt"""
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt 存在")
        
        with open('requirements.txt', 'r') as f:
            content = f.read()
            print("📦 依赖包列表:")
            for line in content.strip().split('\n'):
                if line.strip():
                    print(f"   - {line.strip()}")
    else:
        print("❌ requirements.txt 不存在")
        return False
    
    return True

def check_git_status():
    """检查Git状态"""
    if os.path.exists('.git'):
        print("✅ Git仓库已初始化")
        
        try:
            # 检查是否有未提交的更改
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print("⚠️  有未提交的更改:")
                print(result.stdout)
            else:
                print("✅ 所有更改已提交")
            
            # 检查远程仓库
            result = subprocess.run(['git', 'remote', '-v'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print("✅ 远程仓库已配置:")
                print(result.stdout)
            else:
                print("⚠️  未配置远程仓库")
                
        except Exception as e:
            print(f"⚠️  Git检查失败: {e}")
    else:
        print("❌ Git仓库未初始化")
        return False
    
    return True

def check_streamlit_config():
    """检查Streamlit配置"""
    if os.path.exists('.streamlit/config.toml'):
        print("✅ Streamlit配置文件存在")
    else:
        print("⚠️  Streamlit配置文件不存在（可选）")

def test_app_locally():
    """测试应用是否可以本地运行"""
    print("\n🧪 测试应用本地运行...")
    try:
        # 尝试导入并运行基本检查
        import streamlit as st
        import option_screener_gui
        print("✅ 应用可以正常导入")
        
        # 检查主要函数是否存在
        functions_to_check = [
            'get_stock_data',
            'analyze_and_filter_puts', 
            'analyze_and_filter_calls',
            'screen_options_gui'
        ]
        
        for func_name in functions_to_check:
            if hasattr(option_screener_gui, func_name):
                print(f"✅ 函数 {func_name} 存在")
            else:
                print(f"❌ 函数 {func_name} 不存在")
                
    except Exception as e:
        print(f"❌ 应用测试失败: {e}")
        return False
    
    return True

def main():
    """主诊断函数"""
    print("🔍 开始部署问题诊断...\n")
    
    issues = []
    
    # 检查各项
    print("=" * 50)
    print("1. 检查Python环境")
    print("=" * 50)
    check_python_version()
    
    print("\n" + "=" * 50)
    print("2. 检查依赖包")
    print("=" * 50)
    if not check_required_packages():
        issues.append("缺少必需的依赖包")
    
    print("\n" + "=" * 50)
    print("3. 检查项目文件")
    print("=" * 50)
    if not check_main_file():
        issues.append("主文件问题")
    
    if not check_requirements_file():
        issues.append("requirements.txt问题")
    
    print("\n" + "=" * 50)
    print("4. 检查Git状态")
    print("=" * 50)
    if not check_git_status():
        issues.append("Git配置问题")
    
    print("\n" + "=" * 50)
    print("5. 检查Streamlit配置")
    print("=" * 50)
    check_streamlit_config()
    
    print("\n" + "=" * 50)
    print("6. 测试应用")
    print("=" * 50)
    if not test_app_locally():
        issues.append("应用运行问题")
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 诊断总结")
    print("=" * 50)
    
    if not issues:
        print("🎉 所有检查通过！应用应该可以正常部署")
        print("\n📋 部署步骤:")
        print("1. git push 推送到GitHub")
        print("2. 访问 share.streamlit.io")
        print("3. 创建新应用并选择你的仓库")
        print("4. 主文件路径: option_screener_gui.py")
        print("5. 点击Deploy!")
    else:
        print("❌ 发现以下问题需要解决:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        
        print("\n💡 解决建议:")
        print("- 安装缺失的依赖包")
        print("- 检查文件路径和名称")
        print("- 确保Git仓库配置正确")
        print("- 测试应用本地运行")

if __name__ == "__main__":
    main()