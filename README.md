# QDC

Overview  
90Yのベータ線スペクトラムの解析フィット用のプログラム。
* plot,kplot・・・生データ描画
* Calibration_mf・・・フィッティング
* simulation_Y90・・・シミュレーション

# Requirement
* ROOT by CERN (for Calibration_mf.py)
* Python module (numpy, matplotlib)
* Cython for(ver_cython)

# Usage
cxx: root -l plot\(run_number\)  
py : python Calibration_mf.py  
pyx : python setup.py ext_build --> python Calibration_cf.py
