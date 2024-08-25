import scipy.stats as stats

# 各真値に対する事後分布の確率密度を計算
def posterior_pdf(p, alpha, beta):
    return stats.beta.pdf(p, alpha, beta)