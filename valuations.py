# -*- coding: utf-8 -*-
import numpy as np

def discount_cash_flow(fcf, proj_rate1, proj_rate2, discount, shares, beta):
    '''
    Discounted Cash Flow formula for intrinsic value based on the projected growth of free cash flow discounted
    back to the present day
    
    :param fcf: A list/array of free cash flow values from the stock's previous annual filings (in millions USD)
    :param proj_rate1: projected % rate of growth for first 10 year period (in decimal form, e.g. 9% growth = 0.09)
    :param proj_rate2: projected % rate of growth for second 10 year period (in decimal form)
    :param discount: the expected % rate of return chosen for this stock (in decimal form)
    :param shares: the number of shares outstanding for the stock (in millions)
    :param beta: the beta coefficient for the stock under analysis
    :return: first, the compound annual growth rate; second and third, the intrinsic value ranges 
      using the given and capital asset pricing model discount rates, respectively
    '''
    fcf = np.array(fcf).astype(float)
    n = len(fcf)-1
    if fcf[0] < 0:
        fcf[0] = np.mean(fcf)
    cagr = (((fcf[n]/fcf[0])**(1.0/n)) - 1) #Compound Annual Growth Rate
    val1numbers = np.zeros(shape=100)
    val2numbers = np.zeros(shape=100)
    #Capital Asset Pricing Model discount rate; 2.5 and 9.11 are estimates for risk free rate and historic stock market return, respectively
    d = (2.5+beta*(9.11-2.5))/100.0
    
    '''
    Note that the values pulled from normal distribution in the loop here are meant to represent random error.
    While normal distribution is not always the most accurate representation of reality, 
    it is helpful for simulating realistic fluctuations in free cash flow growth. 
    ''' 
    for i in xrange(0,100):
        proj=fcf[9]*((1+proj_rate1)**(np.arange(1,11)))+np.random.normal(scale=np.std(fcf,ddof=1),size=10)
        proj2=proj[9]*((1+proj_rate2)**(np.arange(1,11)))+np.random.normal(scale=np.std(fcf,ddof=1),size=10)
        projtotal=np.concatenate([proj,proj2])
        dis = projtotal/((1+discount)**np.arange(1,21))
        dis2 = projtotal/((1+d)**np.arange(1,21))
        val1 = np.sum(dis)/shares
        val1numbers[i] = val1
        val2=sum(dis2)/shares
        val2numbers[i] = val2
    return cagr, val1numbers, val2numbers
    
def ben_graham_formula(eps, proj_growth, risk_free_rate=0.025, safe_eps=False, safe_growth=False, adjust=True):
    '''
    Benjamin Graham formula for intrinsic value based on projected earnings per share growth
    
    :param eps: the current earnings per share of the stock under analysis
    :param proj_growth: projected % growth rate of the stock (in decimal form, e.g. 9% growth = 0.09) 
    :param risk_free_rate: the current risk free interest rate, usually the 30 year AAA treasury bond interest rate (in decimal form)
    :param safe_eps: boolean value for using a more conservative estimate for a company's EPS under 0% growth
    :param safe_growth: boolean value for using a more conservative growth multiplier for a company's EPS
    :param adjust: boolean value for using adjusted value calculation by starting with average EPS instead of last period's EPS
    :return: first, the intrinsic value calculation based on the given parameters; 
      second, the adjusted intrinsic value using average EPS (if specified)
    '''
    eps = np.array(eps)
    adjusted_eps = np.mean(eps) if adjust else None
    const = 7 if safe.eps else 8
    g = 1.5 if safe_growth else 2
    
    val = (eps[10]*(const+g*(proj_growth*100)*4.4))/(risk_free_rate*100)
    if adjust:
        val_adj = (adjust*(const+g*(proj_growth*100)*4.4))/(risk_free_rate*100)
    else:
        val_adj = None
    return val, val_adj
  
def div_discount_model(current_div, discount, div_growth_rate1, div_period1=5, div_growth_rate2, div_period2=5, const_growth):
    '''
    Dividend Discount Model for intrinsic value based on projected dividend growth across multiple time periods
    
    :param current_div: the current annual dividend amount of a stock in USD
    :param discount: the required rate of return for the stock under analysis
    :param div_growth_rate1: the projected dividend growth rate % for the first time period
    :param div_period1: the number of years the dividend will grow at div_growth_rate1
    :param div_growth_rate2: the projected dividend growth rate % for the second time period
    :param div_period2: the number of years the dividend will grow at div_growth_rate2
    :param const_growth: the assumed indefinite growth rate for the stock after the initial growth periods have passed;
      must be less than the discount rate
    :return the intrinsic value calculation using multistage dividend growth
    '''
    proj1 = current_div*((1.0+div_growth_rate1)**np.arange(1,div_period1+1))
    proj2 = proj1[len(proj1)-1]*((1.0+div_growth_rate2)**np.arange(1,div_period2+1))
    const = np.array([(proj2[len(proj2)-1]*(1+const_growth))/(discount - const_growth)])
    dis = np.concatenate([proj1,proj2,const])/((1+discount)**np.arange(1,len(proj1)+len(proj2)+len(const)+1))
    val = dis.sum()    
    return val
        
def gordon_growth_model(current_div, const_growth, discount):
    '''
    Gordon growth model for calculating intrisinic value based on a constant dividend growth
    
    :param current_div: the current annual dividend amount of a stock in USD
    :param const_growth: the constant % growth rate for the annual dividend (in decimal form, e.g. 9% growth = 0.09)
    :param discount: required % rate of return for the stock (in decimal form); must be greater than the constant growth rate
    :return: the calculated instrinsic value for the stock
    '''
    return (current_div*(1+const_growth))/(discount-const_growth)