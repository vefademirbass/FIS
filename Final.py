import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import datetime

# 1. TEMEL DEĞİŞKENLER VE ÜYELİK FONKSİYONLARI

x_sev = np.arange(0, 11, 1)
x_acc = np.arange(0, 11, 1)
x_pop = np.arange(0, 11, 1)
x_pri = np.arange(0, 101, 1)

x_vars = {'severity': x_sev, 'accessibility': x_acc, 'population': x_pop, 'priority': x_pri}
mfs = {'severity': {}, 'accessibility': {}, 'population': {}, 'priority': {}}


# Severity (Hasar): Düşük için Üçgen, Orta için Çan (Gauss), Yüksek için Yamuk (Trap)
mfs['severity']['low'] = fuzz.trimf(x_sev, [0, 0, 5])
mfs['severity']['medium'] = fuzz.gaussmf(x_sev, 5, 1.5)
mfs['severity']['high'] = fuzz.trapmf(x_sev, [5, 8, 10, 10])

# Accessibility (Ulaşım): Kötü için Yamuk, Orta ve İyi için Üçgen
mfs['accessibility']['poor'] = fuzz.trapmf(x_acc, [0, 0, 2, 5])
mfs['accessibility']['moderate'] = fuzz.trimf(x_acc, [2, 5, 8])
mfs['accessibility']['good'] = fuzz.trimf(x_acc, [5, 10, 10])

# Population (Nüfus): Düşük ve Orta için Gauss, Yüksek için Yamuk
mfs['population']['low'] = fuzz.gaussmf(x_pop, 0, 2)
mfs['population']['medium'] = fuzz.gaussmf(x_pop, 5, 2)
mfs['population']['high'] = fuzz.trapmf(x_pop, [6, 8, 10, 10])

# Priority (Öncelik):
mfs['priority']['low'] = fuzz.trimf(x_pri, [0, 0, 30])
mfs['priority']['medium'] = fuzz.trimf(x_pri, [20, 40, 60])
mfs['priority']['medium_high'] = fuzz.trimf(x_pri, [40, 60, 80])
mfs['priority']['high'] = fuzz.trimf(x_pri, [60, 80, 90])
mfs['priority']['very_high'] = fuzz.trapmf(x_pri, [80, 90, 100, 100])


# 2. KURAL TABANI OLUŞTURMA (27 KURAL)

def get_rule_consequent(s_level, a_level, p_level):
    score = 0
    if s_level == 'high': score += 3
    elif s_level == 'medium': score += 2
    else: score += 1
    
    if p_level == 'high': score += 3
    elif p_level == 'medium': score += 2
    else: score += 1
    
    if a_level == 'good': score += 3
    elif a_level == 'moderate': score += 2
    else: score += 1 

    if score >= 8: return 'very_high'
    elif score >= 7: return 'high'
    elif score >= 6: return 'medium_high'
    elif score >= 5: return 'medium'
    else: return 'low'

rules_dict = {}
rule_idx = 1
for s in ['low', 'medium', 'high']:
    for a in ['poor', 'moderate', 'good']:
        for p in ['low', 'medium', 'high']:
            out_label = get_rule_consequent(s, a, p)
            rules_dict[f'R{rule_idx}'] = {'s_level': s, 'a_level': a, 'p_level': p, 'out_level': out_label}
            rule_idx += 1


# 3. SENTETİK VERİ ÜRETİMİ 

np.random.seed(42)
NUM_SAMPLES = 500 # Toplam 1500 veri 
data_list = []

print(f"\n--- Generating Multi-Hazard Synthetic Data ({NUM_SAMPLES*3} samples) ---")

# Verilerin hedefleri (Gerçek Uzman Skoru) için basit bir referans kural tabanı kuruyoruz
sev_ctrl = ctrl.Antecedent(x_sev, 'severity')
acc_ctrl = ctrl.Antecedent(x_acc, 'accessibility')
pop_ctrl = ctrl.Antecedent(x_pop, 'population')
pri_ctrl = ctrl.Consequent(x_pri, 'priority')

for label in ['low', 'medium', 'high']:
    sev_ctrl[label] = mfs['severity'][label]
    pop_ctrl[label] = mfs['population'][label]
for label in ['poor', 'moderate', 'good']:
    acc_ctrl[label] = mfs['accessibility'][label]
for label in ['low', 'medium', 'medium_high', 'high', 'very_high']:
    pri_ctrl[label] = mfs['priority'][label]

sim_rules = []
for r_id, r in rules_dict.items():
    sim_rules.append(ctrl.Rule(sev_ctrl[r['s_level']] & acc_ctrl[r['a_level']] & pop_ctrl[r['p_level']], pri_ctrl[r['out_level']]))

expert_sim = ctrl.ControlSystemSimulation(ctrl.ControlSystem(sim_rules))

def generate_data(hazard_type, sev_func, acc_func, pop_func):
    for i in range(NUM_SAMPLES):
        # Dağılımlar 0-10 arası
        val_sev = round(np.clip(sev_func(), 0, 10), 1)
        val_acc = round(np.clip(acc_func(), 0, 10), 1)
        val_pop = round(np.clip(pop_func(), 0, 10), 1)

        expert_sim.input['severity'] = val_sev
        expert_sim.input['accessibility'] = val_acc
        expert_sim.input['population'] = val_pop
        try:
            expert_sim.compute()
            target_score = expert_sim.output['priority']
        except:
            target_score = 0.0

        data_list.append({
            "Hazard_Type": hazard_type,
            "Severity": val_sev,
            "Accessibility": val_acc,
            "Population": val_pop,
            "Target_Priority_Score": round(target_score, 2)
        })


# Deprem (Beta - Sola çarpık, yüksek hasar), Sel (Normal/Gauss), Yangın (Exponential/Üstel)
generate_data("Earthquake", lambda: np.random.beta(8, 2)*10, lambda: np.random.beta(2, 8)*10, lambda: np.random.normal(6, 2))
generate_data("Flood", lambda: np.random.normal(5, 2.5), lambda: np.random.normal(4, 2), lambda: np.random.normal(5, 3))
generate_data("Wildfire", lambda: np.random.exponential(4), lambda: np.random.normal(5, 3), lambda: np.random.exponential(3))

df = pd.DataFrame(data_list).sample(frac=1, random_state=42).reset_index(drop=True)


# 4. AĞIRLIK VE ÇIKARIM ALGORİTMALARI

def calculate_rule_weights(df_train, rules_dict, x_vars, mfs):
    weights = {}
    N = len(df_train)
    for rule_id, rule in rules_dict.items():
        sum_alpha = 0
        sum_alpha_beta = 0
        for index, row in df_train.iterrows():
            mu_s = fuzz.interp_membership(x_vars['severity'], mfs['severity'][rule['s_level']], row['Severity'])
            mu_a = fuzz.interp_membership(x_vars['accessibility'], mfs['accessibility'][rule['a_level']], row['Accessibility'])
            mu_p = fuzz.interp_membership(x_vars['population'], mfs['population'][rule['p_level']], row['Population'])
            
            alpha_ir = min(mu_s, mu_a, mu_p) # Antecedent Compatibility
            beta_ir = fuzz.interp_membership(x_vars['priority'], mfs['priority'][rule['out_level']], row['Target_Priority_Score'])
            
            sum_alpha += alpha_ir
            sum_alpha_beta += (alpha_ir * beta_ir)
            
        support_r = sum_alpha / N if N > 0 else 0
        confidence_r = (sum_alpha_beta / sum_alpha) if sum_alpha > 0 else 0
        weights[rule_id] = confidence_r * support_r
        
    # Ağırlıkları normalize et (0-1 arası)
    max_w = max(weights.values()) if weights.values() else 1.0
    for k in weights: weights[k] = round(weights[k] / max_w, 4) if max_w > 0 else 0
    return weights

def weighted_fuzzy_inference(row, rules_dict, weights_dict, x_vars, mfs):
    aggregated_output = np.zeros_like(x_vars['priority'])
    for rule_id, rule in rules_dict.items():
        mu_s = fuzz.interp_membership(x_vars['severity'], mfs['severity'][rule['s_level']], row['Severity'])
        mu_a = fuzz.interp_membership(x_vars['accessibility'], mfs['accessibility'][rule['a_level']], row['Accessibility'])
        mu_p = fuzz.interp_membership(x_vars['population'], mfs['population'][rule['p_level']], row['Population'])
        
        alpha = min(mu_s, mu_a, mu_p)
        alpha_prime = weights_dict[rule_id] * alpha # Weighted Firing Strength
        
        rule_activation = np.fmin(alpha_prime, mfs['priority'][rule['out_level']])
        aggregated_output = np.fmax(aggregated_output, rule_activation)
        
    if np.sum(aggregated_output) == 0: return 0.0
    return fuzz.defuzz(x_vars['priority'], aggregated_output, 'centroid')


# 5. GROUP K-FOLD CROSS VALIDATION 

print("\n--- Starting Group K-Fold Cross-Validation ---")
gkf = GroupKFold(n_splits=3)
groups = df['Hazard_Type']

fold_no = 1
results_log = []

for train_idx, test_idx in gkf.split(df, df['Target_Priority_Score'], groups):
    df_train = df.iloc[train_idx]
    df_test = df.iloc[test_idx]
    
    test_hazard = df_test['Hazard_Type'].iloc[0]
    train_hazards = df_train['Hazard_Type'].unique().tolist()
    
    print(f"\n[FOLD {fold_no}] Training on: {train_hazards} | Testing on Unseen: {test_hazard}")
    
    # 1. Kural Ağırlıklarını Öğren (Sadece Eğitim Verisiyle)
    weights = calculate_rule_weights(df_train, rules_dict, x_vars, mfs)
    
    # 2. Görmediği Afeti Test Et
    y_true = []
    y_pred = []
    for index, row in df_test.iterrows():
        y_true.append(row['Target_Priority_Score'])
        y_pred.append(weighted_fuzzy_inference(row, rules_dict, weights, x_vars, mfs))
        
    # 3. Metrikleri Hesapla
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    print(f"Results -> RMSE: {rmse:.2f} | MAE: {mae:.2f} | R2 Score: {r2:.3f}")
    
    results_log.append({"Fold": fold_no, "Test_Hazard": test_hazard, "RMSE": rmse, "MAE": mae, "R2": r2})
    fold_no += 1


# 6. EXCEL'E KAYDETME

zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M")
excel_name = f"MultiHazard_Results_{zaman}.xlsx"
df.to_excel(excel_name, index=False)
print(f"\nFull dataset saved to: {excel_name}")
print("================ DONE ================")