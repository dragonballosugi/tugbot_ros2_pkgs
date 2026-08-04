# tugbot_ros2_pkgs

ROS 2 Jazzy環境で、TugbotのGazeboシミュレーション、SLAMによる地図作成、Navigation2による自律移動を行うためのパッケージ群です。

1. `ros2_ws/src`へcloneする
2. Gazebo上でTugbotを動かして自分の地図を作る
3. 地図を決められた`map`ディレクトリへ保存する
4. 作成した地図でNavigation2を実行する


## 対象環境

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic

## 1. `ros2_ws/src`へcloneする


```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/dragonballosugi/tugbot_ros2_pkgs.git
cd ..
colcon build 
source install/setup.bash
```




## 2. SLAMで自分の地図を作る

### 1つ目のターミナル：TugbotをGazeboに表示する

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch tugbot_gazebo tugbot_depot.launch.py
```

Gazeboの画面が出たら忘れずシミュレーションをスタートさせておくこと。（左下の▷再生マークを押す）


### 2つ目のターミナル：キーボードテレオペレーションを起動する

```bash
source ~/ros2_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r /cmd_vel:=/model/tugbot/cmd_vel
```

このターミナルを選択した状態で、画面に表示されるキーを使ってTugbotを移動させます。

### 3つ目のターミナル：SLAM Toolboxを起動する

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch tugbot_slam slam_toolbox.launch.py
```

キーボードでTugbotを少しずつ移動させ、壁や通路を十分に観測して地図を作成します。

## 3. 作成した地図を保存する

補足：既存の`map.yaml`と`map.pgm`がある場合は、先に元のファイルを削除してください。

地図を作り終えたら、SLAM Toolboxを動かしたまま別のターミナルで次を実行します。`-f`にはファイル名の`map`まで指定します。拡張子は付けません。

```bash
source ~/ros2_ws/install/setup.bash
ros2 run nav2_map_server map_saver_cli \
  -f ~/ros2_ws/src/tugbot_ros2_pkgs/tugbot_navigation2/map/map
```


## 4. 作成した地図でNavigation2を実行する

地図ファイルを保存したあと、`tugbot_navigation2`を再ビルドして新しい地図をinstall側へ反映します。

```bash
cd ~/ros2_ws
colcon build --packages-select tugbot_navigation2
source install/setup.bash
```

### 1つ目のターミナル：Gazeboを起動する

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch tugbot_gazebo tugbot_depot.launch.py
```

Gazeboの画面が出たら忘れずシミュレーションをスタートさせておくこと。（左下の▷再生マークを押す）

### 2つ目のターミナル：Navigation2を起動する

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch tugbot_navigation2 navigation2.launch.py
```

rvizが立ち上がった後に「2D Pose Estimate」で自己位置を指定すると移動ロボットの周りに点群が出て自己位置が推定されていることが分かります。

「Navigation2 Goal」をクリックしてから、目標位置を指定すると経路計画をしてくれて目標位置まで移動します。
