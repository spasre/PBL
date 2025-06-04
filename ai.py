# 变速圆周运动小球动画实验（可调参数）
from vpython import *

# 可调参数
mass = 1.0         # 小球质量 (kg)
radius = 2.0       # 圆周半径 (m)
v0 = 1.0           # 初始线速度 (m/s)
alpha = 0.2        # 角加速度 (rad/s^2)
ball_radius = 0.1  # 小球半径 (m)

# 场景设置
scene = canvas(title="变速圆周运动小球实验", width=800, height=600, background=color.white)

# 绘制圆轨道
circle = ring(pos=vector(0,0,0), axis=vector(0,0,1), radius=radius, thickness=0.01, color=color.gray(0.7))

# 创建小球
ball = sphere(pos=vector(0,radius,0), radius=ball_radius, color=color.red, make_trail=True, trail_type="curve", interval=10, retain=200)

# 速度箭头
arrow_v = arrow(pos=ball.pos, axis=vector(0,0,0), color=color.blue, shaftwidth=0.05)
# 向心力箭头
arrow_c = arrow(pos=ball.pos, axis=vector(0,0,0), color=color.green, shaftwidth=0.05)

g = 9.8  # 重力加速度 (m/s^2)

# 初始角度和角速度
ball.theta = 0.5  # 最高点
omega = 0       # 初始角速度为0
mass = 0.1  # 小球质量 (kg)

dt = 0.001

# 控制参数
# from vpython import wtext, winput, button, scene, slider

# 状态变量
is_running = False

# 控件回调

def set_theta(s):
    global ball, omega
    if not is_running:
        ball.theta = s.value
        x = radius * sin(ball.theta)
        y = radius * cos(ball.theta)
        ball.pos = vector(x, y, 0)
        arrow_v.pos = ball.pos
        arrow_c.pos = ball.pos

def set_omega(s):
    global omega
    if not is_running:
        omega = s.value

def toggle_run():
    global is_running
    is_running = not is_running
    if is_running:
        btn_run.text = "暂停"
    else:
        btn_run.text = "播放"

def start_motion():
    global is_running, omega
    is_running = True
    btn_run.text = "暂停"
    omega = slider_omega.value

# 控件布局
scene.append_to_caption("\n初始角度(弧度): ")
slider_theta = slider(min=-pi, max=pi, value=0.5, length=220, bind=set_theta, right=15)
scene.append_to_caption("\n初始角速度(rad/s): ")
slider_omega = slider(min=-5, max=5, value=0, length=220, bind=set_omega, right=15)
scene.append_to_caption("\n")
btn_run = button(text="播放", bind=toggle_run)
scene.append_to_caption("    ")
btn_start = button(text="重置并开始", bind=start_motion)
scene.append_to_caption("\n")

# 初始设置
ball.theta = slider_theta.value
omega = slider_omega.value
x = radius * sin(ball.theta)
y = radius * cos(ball.theta)
ball.pos = vector(x, y, 0)
arrow_v.pos = ball.pos
arrow_c.pos = ball.pos

while True:
    rate(500)
    if not is_running:
        continue
    # 重力在切向的分量: m * g * sin(theta)
    tangential_acc = g * sin(ball.theta)  # 负号保证顺时针为正方向
    # 角加速度 alpha = a_t / r
    alpha = tangential_acc / radius
    # 更新角速度和角度
    omega += alpha * dt
    ball.theta += omega * dt
    # 计算新位置
    x = radius * sin(ball.theta)
    y = radius * cos(ball.theta)
    ball.pos = vector(x, y, 0)
    # 更新速度箭头
    v = omega * radius
    vx = v * cos(ball.theta)
    vy = -v * sin(ball.theta)
    arrow_v.pos = ball.pos
    arrow_v.axis = vector(vx, vy, 0) * 0.2
    # 更新向心力箭头
    centripetal_force = mass * (omega ** 2) * radius
    arrow_c.pos = ball.pos
    arrow_c.axis = vector(-x, -y, 0) / sqrt(x**2 + y**2) * centripetal_force
