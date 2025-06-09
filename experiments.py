# 物理实验示例脚本
# 展示如何使用增强版圆周运动项目进行各种实验

import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class PhysicsExperiments:
    """物理实验类，包含各种预设实验"""
    
    def __init__(self):
        self.data_storage = {}
        
    def energy_conservation_demo(self):
        """能量守恒定律演示实验"""
        print("=== 能量守恒定律演示实验 ===")
        print("实验目的：验证机械能守恒定律")
        print("实验步骤：")
        print("1. 设置小球从高位置（θ=90°）静止释放")
        print("2. 观察动能和势能的相互转换")
        print("3. 验证总能量保持恒定")
        print("4. 记录能量数据并分析")
        
        # 实验参数
        params = {
            'initial_theta': 1.57,  # 90度
            'initial_omega': 0,     # 静止释放
            'mass': 0.1,           # 质量
            'radius': 2.0,         # 半径
            'gravity': 9.8         # 重力加速度
        }
        
        print(f"\n实验参数：")
        for key, value in params.items():
            print(f"  {key}: {value}")
            
        return params
    
    def mass_comparison_experiment(self):
        """质量对比实验"""
        print("=== 质量对比实验 ===")
        print("实验目的：研究质量对圆周运动的影响")
        print("实验步骤：")
        print("1. 设置三个不同质量的小球")
        print("2. 使用相同的初始条件")
        print("3. 对比运动周期和轨迹")
        print("4. 验证周期与质量的关系")
        
        # 三组不同质量的小球
        experiments = [
            {'name': '轻球', 'mass': 0.05, 'theta': 0.5, 'omega': 0},
            {'name': '中球', 'mass': 0.10, 'theta': 0.5, 'omega': 0},
            {'name': '重球', 'mass': 0.20, 'theta': 0.5, 'omega': 0}
        ]
        
        print(f"\n实验配置：")
        for exp in experiments:
            print(f"  {exp['name']}: 质量={exp['mass']}kg, θ={exp['theta']}rad, ω={exp['omega']}rad/s")
            
        return experiments
    
    def initial_velocity_study(self):
        """初始速度影响研究"""
        print("=== 初始速度影响研究 ===")
        print("实验目的：分析初始角速度对运动的影响")
        print("实验步骤：")
        print("1. 设置不同的初始角速度")
        print("2. 从相同位置释放")
        print("3. 观察运动轨迹差异")
        print("4. 分析临界速度条件")
        
        # 不同初始速度的实验
        velocity_tests = [
            {'name': '低速', 'omega': 0.5, 'description': '摆动运动'},
            {'name': '中速', 'omega': 2.0, 'description': '过渡状态'},
            {'name': '高速', 'omega': 4.0, 'description': '完整圆周运动'}
        ]
        
        print(f"\n速度测试：")
        for test in velocity_tests:
            print(f"  {test['name']}: ω={test['omega']}rad/s - {test['description']}")
            
        return velocity_tests
    
    def gravity_environment_comparison(self):
        """不同重力环境对比实验"""
        print("=== 不同重力环境对比实验 ===")
        print("实验目的：模拟不同天体环境下的运动")
        print("实验步骤：")
        print("1. 设置不同的重力加速度")
        print("2. 使用相同的初始条件")
        print("3. 对比运动周期和能量")
        print("4. 分析重力对运动的影响")
        
        # 不同天体环境
        environments = [
            {'name': '月球', 'gravity': 1.62, 'description': '低重力环境'},
            {'name': '地球', 'gravity': 9.81, 'description': '标准重力环境'},
            {'name': '木星', 'gravity': 24.79, 'description': '高重力环境'}
        ]
        
        print(f"\n环境设置：")
        for env in environments:
            print(f"  {env['name']}: g={env['gravity']}m/s² - {env['description']}")
            
        return environments
    
    def analyze_exported_data(self, csv_filename):
        """分析导出的实验数据"""
        print(f"=== 数据分析：{csv_filename} ===")
        
        try:
            # 读取CSV数据
            data = []
            with open(csv_filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            
            if not data:
                print("错误：文件为空或格式不正确")
                return
            
            # 提取数据
            times = [float(row['时间(s)']) for row in data]
            angles = [float(row['角度(rad)']) for row in data]
            velocities = [float(row['速度(m/s)']) for row in data]
            kinetic_energies = [float(row['动能(J)']) for row in data]
            potential_energies = [float(row['势能(J)']) for row in data]
            total_energies = [float(row['总能量(J)']) for row in data]
            
            # 基本统计
            print(f"数据点数：{len(data)}")
            print(f"时间范围：{min(times):.2f}s - {max(times):.2f}s")
            print(f"角度范围：{min(angles):.3f}rad - {max(angles):.3f}rad")
            print(f"最大速度：{max(velocities):.3f}m/s")
            
            # 能量分析
            avg_total_energy = sum(total_energies) / len(total_energies)
            energy_variation = max(total_energies) - min(total_energies)
            energy_stability = (energy_variation / avg_total_energy) * 100
            
            print(f"\n能量分析：")
            print(f"平均总能量：{avg_total_energy:.6f}J")
            print(f"能量变化：{energy_variation:.6f}J")
            print(f"能量稳定性：{energy_stability:.3f}%")
            
            # 绘制图表
            self.plot_analysis(times, angles, velocities, kinetic_energies, 
                             potential_energies, total_energies, csv_filename)
            
            return {
                'times': times,
                'angles': angles,
                'velocities': velocities,
                'energies': {
                    'kinetic': kinetic_energies,
                    'potential': potential_energies,
                    'total': total_energies
                },
                'stats': {
                    'avg_total_energy': avg_total_energy,
                    'energy_variation': energy_variation,
                    'energy_stability': energy_stability
                }
            }
            
        except FileNotFoundError:
            print(f"错误：找不到文件 {csv_filename}")
            return None
        except Exception as e:
            print(f"错误：数据分析失败 - {e}")
            return None
    
    def plot_analysis(self, times, angles, velocities, ke, pe, te, filename):
        """绘制分析图表"""
        
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'实验数据分析 - {filename}', fontsize=14)
        
        # 角度随时间变化
        axes[0, 0].plot(times, angles, 'b-', linewidth=2)
        axes[0, 0].set_title('角度变化')
        axes[0, 0].set_xlabel('时间 (s)')
        axes[0, 0].set_ylabel('角度 (rad)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 速度随时间变化
        axes[0, 1].plot(times, velocities, 'r-', linewidth=2)
        axes[0, 1].set_title('速度变化')
        axes[0, 1].set_xlabel('时间 (s)')
        axes[0, 1].set_ylabel('速度 (m/s)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 能量随时间变化
        axes[1, 0].plot(times, ke, 'r-', label='动能', linewidth=2)
        axes[1, 0].plot(times, pe, 'b-', label='势能', linewidth=2)
        axes[1, 0].plot(times, te, 'g-', label='总能量', linewidth=2)
        axes[1, 0].set_title('能量变化')
        axes[1, 0].set_xlabel('时间 (s)')
        axes[1, 0].set_ylabel('能量 (J)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 相位图（角度 vs 角速度）
        # 计算角速度（数值微分）
        angular_velocities = []
        for i in range(1, len(angles)):
            dt = times[i] - times[i-1]
            dtheta = angles[i] - angles[i-1]
            angular_velocities.append(dtheta / dt if dt > 0 else 0)
        
        if angular_velocities:
            axes[1, 1].plot(angles[1:], angular_velocities, 'purple', linewidth=1, alpha=0.7)
            axes[1, 1].set_title('相位图')
            axes[1, 1].set_xlabel('角度 (rad)')
            axes[1, 1].set_ylabel('角速度 (rad/s)')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 保存图片
        plot_filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        print(f"分析图表已保存为：{plot_filename}")
        
        plt.show()
    
    def generate_experiment_report(self, experiment_name, data_analysis):
        """生成实验报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_filename = f"experiment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("圆周运动物理实验报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"实验名称：{experiment_name}\n")
            f.write(f"实验时间：{timestamp}\n")
            f.write(f"数据点数：{len(data_analysis['times'])}\n")
            f.write("\n")
            
            f.write("实验结果分析：\n")
            f.write("-" * 30 + "\n")
            stats = data_analysis['stats']
            f.write(f"平均总能量：{stats['avg_total_energy']:.6f} J\n")
            f.write(f"能量变化幅度：{stats['energy_variation']:.6f} J\n")
            f.write(f"能量守恒精度：{100-stats['energy_stability']:.3f}%\n")
            f.write("\n")
            
            f.write("物理量统计：\n")
            f.write("-" * 30 + "\n")
            f.write(f"最大动能：{max(data_analysis['energies']['kinetic']):.6f} J\n")
            f.write(f"最大势能：{max(data_analysis['energies']['potential']):.6f} J\n")
            f.write(f"最大速度：{max(data_analysis['velocities']):.3f} m/s\n")
            f.write(f"角度范围：{min(data_analysis['angles']):.3f} - {max(data_analysis['angles']):.3f} rad\n")
            f.write("\n")
            
            f.write("结论：\n")
            f.write("-" * 30 + "\n")
            if stats['energy_stability'] < 1.0:
                f.write("✓ 能量守恒定律得到很好的验证\n")
            elif stats['energy_stability'] < 5.0:
                f.write("✓ 能量基本守恒，存在小幅数值误差\n")
            else:
                f.write("⚠ 能量守恒存在较大偏差，需检查实验设置\n")
            
            f.write("\n实验建议：\n")
            f.write("-" * 30 + "\n")
            f.write("1. 减小时间步长可提高数值精度\n")
            f.write("2. 延长实验时间可观察更多周期\n")
            f.write("3. 对比不同初始条件的实验结果\n")
            
        print(f"实验报告已生成：{report_filename}")
        return report_filename

# 示例使用方法
def main():
    """主函数 - 演示实验脚本的使用"""
    
    experiments = PhysicsExperiments()
    
    print("=" * 60)
    print("物理实验示例脚本")
    print("=" * 60)
    
    # 显示各种实验设置
    experiments.energy_conservation_demo()
    print("\n" + "-" * 60 + "\n")
    
    experiments.mass_comparison_experiment()
    print("\n" + "-" * 60 + "\n")
    
    experiments.initial_velocity_study()
    print("\n" + "-" * 60 + "\n")
    
    experiments.gravity_environment_comparison()
    print("\n" + "-" * 60 + "\n")
    
    # 数据分析示例
    print("数据分析功能演示：")
    print("请先运行 ai_enhanced.py，记录数据并导出CSV文件")
    print("然后调用 analyze_exported_data() 函数分析数据")
    
    # 示例CSV文件名（需要用户实际生成）
    example_csv = "physics_data_example.csv"
    print(f"示例用法：experiments.analyze_exported_data('{example_csv}')")

if __name__ == "__main__":
    main() 