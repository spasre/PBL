# 实验配置文件
# 这个文件包含了所有可自定义的实验参数

class ExperimentConfig:
    """实验配置类"""
    
    # 场景设置
    SCENE_WIDTH = 1200
    SCENE_HEIGHT = 800
    SCENE_BACKGROUND = (1, 1, 1)  # 白色背景
    SCENE_TITLE = "增强版变速圆周运动小球实验"
    
    # 物理参数
    DEFAULT_GRAVITY = 9.8  # 默认重力加速度 (m/s²)
    MIN_GRAVITY = 1.0
    MAX_GRAVITY = 20.0
    
    DEFAULT_RADIUS = 2.0   # 默认圆周半径 (m)
    MIN_RADIUS = 0.5
    MAX_RADIUS = 5.0
    
    # 小球参数
    BALL_RADIUS = 0.08     # 小球显示半径 (m)
    TRAIL_RETAIN = 300     # 轨迹保留点数
    
    # 默认小球配置
    DEFAULT_BALLS = [
        {
            'name': '小球1',
            'mass': 0.1,
            'color': (1, 0, 0),    # 红色
            'initial_theta': 0.5,
            'initial_omega': 0,
        },
        {
            'name': '小球2', 
            'mass': 0.15,
            'color': (0, 0, 1),    # 蓝色
            'initial_theta': 1.0,
            'initial_omega': 0,
        },
        {
            'name': '小球3',
            'mass': 0.2,
            'color': (0, 1, 0),    # 绿色
            'initial_theta': -0.5,
            'initial_omega': 0,
        }
    ]
    
    # 控制参数范围
    THETA_RANGE = (-3.14159, 3.14159)  # 角度范围 (弧度)
    OMEGA_RANGE = (-10, 10)            # 角速度范围 (rad/s)
    MASS_RANGE = (0.05, 1.0)           # 质量范围 (kg)
    
    # 仿真参数
    SIMULATION_DT = 0.002     # 时间步长 (s)
    FRAME_RATE = 500          # 帧率
    
    # 图表设置
    ENABLE_ENERGY_GRAPH = True
    GRAPH_WIDTH = 400
    GRAPH_HEIGHT = 200
    
    # 矢量显示设置
    VELOCITY_ARROW_SCALE = 0.15      # 速度箭头缩放
    FORCE_ARROW_SCALE = 0.05         # 力箭头缩放
    ARROW_SHAFT_WIDTH = 0.03         # 箭头轴宽度
    
    # 数据记录设置
    DATA_PRECISION = {
        'time': 3,
        'angle': 4,
        'angular_velocity': 4,
        'speed': 4,
        'energy': 6,
        'acceleration': 4
    }
    
    # UI设置
    SLIDER_LENGTH = 200
    BUTTON_SPACING = "    "
    
    # 坐标轴设置
    AXIS_LENGTH = 6
    AXIS_COLOR = (0.5, 0.5, 0.5)
    TICK_SIZE = 0.1
    TICK_RANGE = (-2, 3)
    
    # 高级物理模式
    ENABLE_AIR_RESISTANCE = False     # 是否启用空气阻力
    AIR_RESISTANCE_COEFF = 0.01       # 空气阻力系数
    
    ENABLE_FRICTION = False           # 是否启用摩擦力
    FRICTION_COEFF = 0.02             # 摩擦系数
    
    # 实验模式
    EXPERIMENT_MODES = {
        'standard': {
            'name': '标准重力摆',
            'description': '经典的重力驱动圆周运动',
            'gravity': 9.8,
            'air_resistance': False,
            'friction': False
        },
        'space': {
            'name': '太空环境',
            'description': '无重力环境下的圆周运动',
            'gravity': 0.0,
            'air_resistance': False,
            'friction': False
        },
        'high_gravity': {
            'name': '高重力环境',
            'description': '类似木星表面的高重力环境',
            'gravity': 24.8,
            'air_resistance': False,
            'friction': False
        },
        'real_world': {
            'name': '真实环境',
            'description': '包含空气阻力和摩擦的真实环境',
            'gravity': 9.8,
            'air_resistance': True,
            'friction': True
        }
    }

# 预设实验场景
PRESET_SCENARIOS = {
    'energy_conservation': {
        'name': '能量守恒演示',
        'description': '展示机械能守恒定律',
        'balls': [
            {'theta': 1.57, 'omega': 0, 'mass': 0.1},  # 90度静止释放
        ],
        'focus': 'energy'
    },
    
    'mass_comparison': {
        'name': '质量对比实验',
        'description': '对比不同质量小球的运动',
        'balls': [
            {'theta': 1.0, 'omega': 0, 'mass': 0.1},
            {'theta': 1.0, 'omega': 0, 'mass': 0.2},
            {'theta': 1.0, 'omega': 0, 'mass': 0.3},
        ],
        'focus': 'dynamics'
    },
    
    'phase_difference': {
        'name': '相位差分析',
        'description': '分析不同初始条件的相位关系',
        'balls': [
            {'theta': 0.5, 'omega': 0, 'mass': 0.1},
            {'theta': 1.0, 'omega': 0, 'mass': 0.1},
            {'theta': 1.5, 'omega': 0, 'mass': 0.1},
        ],
        'focus': 'oscillation'
    },
    
    'initial_velocity': {
        'name': '初始速度影响',
        'description': '研究初始角速度对运动的影响',
        'balls': [
            {'theta': 0, 'omega': 1, 'mass': 0.1},
            {'theta': 0, 'omega': 2, 'mass': 0.1},
            {'theta': 0, 'omega': 3, 'mass': 0.1},
        ],
        'focus': 'velocity'
    }
}

# 教学模式配置
TEACHING_MODE = {
    'enable_hints': True,
    'show_formulas': True,
    'step_by_step': False,
    'auto_annotations': True
} 