# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/29 08:18
@Author  : Mjy
@Site    : 
@File    : cal_test.py
@Software: PyCharm
"""
import sympy as sp
import numpy as np
import math
from catboost import CatBoostRegressor
# ST, IC, t, n, fc, fu, D_d, Adfu, Acfc, Abtb, t/D^0.5
mean = np.array([[1.18220339,
                  1.25423729,
                  23.70338983,
                  1.48305085,
                  56.06766102,
                  588.57182203,
                  3.37716143,
                  181.70872838,
                  163.08535965,
                  177.45551319,
                  0.61456384]])
mean = mean.T
std = np.array([[1.49005315e-01,
                 1.89600689e-01,
                 7.21365987e+01,
                 6.98865269e-01,
                 1.12968008e+03,
                 2.56072720e+03,
                 7.45478287e-01,
                 7.76810964e+03,
                 1.08022182e+04,
                 2.07066147e+04,
                 1.35451924e-02]])
std = std.T
std = np.sqrt(std)
CatBoost_model = CatBoostRegressor()
CatBoost_model.load_model('CatBoost.bin')

def final_out(ST, IC, n, t, D, d, hp, bp, fc, fu, V_f, L_f, fai_f, a):
    if ST == 1: # ST为 PT
        Ab = 2*(t*hp+hp*bp-np.pi*D**2/4)
    else:  # ST为 SST
        Ab = 2 * (hp * bp - np.pi * D ** 2 / 4)+t * hp
    # 判断是否为UHPC：1是，0否
    if a == 1:
        tb = (0.04+0.04*V_f*L_f/fai_f)*np.sqrt(fc/0.94)
    else:
        tb = 0.48*(-0.054*fc+0.7*np.sqrt(fc)-1.193)
    k = (t/D)**0.5
    D_d = D/d
    Adfu = np.pi * d * d / 4*fu/1000
    Acfc = np.pi * (D * D - d * d) / 4*fc/1000
    Abtb = Ab*tb/1000
    # ST, IC, t, n, fc, fu, D_d, Adfu, Acfc, Abtb, t/D^0.5
    ST_s = (ST - mean[0, 0]) / std[0, 0]
    IC_s = (IC - mean[1, 0]) / std[1, 0]
    t_s = (t - mean[2, 0]) / std[2, 0]
    n_s = (n - mean[3, 0]) / std[3, 0]
    fc_s = (fc - mean[4, 0]) / std[4, 0]
    fu_s = (fu - mean[5, 0]) / std[5, 0]
    D_d_s = (D_d - mean[6, 0]) / std[6, 0]
    Adfu_s = (Adfu - mean[7, 0]) / std[7, 0]
    Acfc_s = (Acfc - mean[8, 0]) / std[8, 0]
    Abtb_s = (Abtb - mean[9, 0]) / std[9, 0]
    k_s = (k - mean[10, 0]) / std[10, 0]
    inp = np.array([ST_s, IC_s, t_s, n_s, fc_s, fu_s, D_d_s, Adfu_s, Acfc_s, Abtb_s, k_s])
    N_u = CatBoost_model.predict(inp)
    return N_u

Nu=final_out(ST = 1, IC = 1,
          n = 1, t = 35,
          D = 70, d = 16,
          hp = 355, bp = 300,
          fc = 48.99, fu = 577.5,
          V_f = 0, L_f = 0, fai_f = 0,
          a = 0)
