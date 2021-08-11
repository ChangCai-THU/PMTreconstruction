import numpy as np
import matplotlib.pyplot as plt

def average(data):
    return np.sum(data)/len(data)
#标准差
def sigma(data,avg):
    sigma_squ=np.sum(np.power((data-avg),2))/len(data)
    return np.power(sigma_squ,0.5)
#高斯分布概率
def prob(data,avg,sig):
    sqrt_2pi=np.power(2*np.pi,0.5)
    coef=1/(sqrt_2pi*sig)
    powercoef=-1/(2*np.power(sig,2))
    mypow=powercoef*(np.power((data-avg),2))
    return coef*(np.exp(mypow))



def lucydconv(lowwave, upwave,loop_times):
    #low是卷积结果，up是卷积中的一个函数，由于这里只有大于0的部分，在传入upwave时第一步先对卷积函数补全
    '''Lucy deconvolution
    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Richardson%E2%80%93Lucy_deconvolution
    .. [2] https://github.com/scikit-image/scikit-image/blob/master/skimage/restoration/deconvolution.py#L329
    '''
    low_deconv = lowwave.copy()
    upwave_mirror = upwave[::-1]#与H转置矩阵相乘等于与卷积函数的镜像进行卷积
    constant = np.sum(upwave)
    low_deconv = low_deconv/constant
    i = 0
    while i<loop_times:
        relative_blur = lowwave / np.convolve(low_deconv, upwave, mode='same')
        new_low_deconv = low_deconv * np.convolve(relative_blur, upwave_mirror, mode='same')
        if np.max(np.abs(low_deconv - new_low_deconv)) < 1e-4:
            break
        else:
            low_deconv = new_low_deconv
            i+=1
    return np.arange(len(low_deconv)), low_deconv,i

# sequence = np.arange(200) 
# up = prob(sequence,50,10)
# up =np.roll(up,+50)
# x = (10**2+5**2)**0.5
# low = prob(sequence,70,x)
#delay = prob(sequence,1,0.5)
#delaysequence = np.arange(-100,100)
#delay = prob(delaysequence,20,5)
#conv = np.convolve(truth,delay,'same')
#plt.plot(truth,color="blue")
#plt.plot(show,color="red")
#plt.plot(delaysequence,delay,color="green")
#plt.plot(conv)
#a = np.sum(show)
#print(np.sum(conv*sequence))
#print(np.sum(truth*sequence))
# plt.plot(sequence,low)
# plt.plot(sequence,up)
# plt.show()
#plt.plot(np.convolve(up,low,mode = 'same'))
# x = lucyddm(low, up,100)
#a = np.array([1,2,3,2,1])
#b = np.array([6,7,8])
#c = np.convolve(a,b,mode = 'same')
# plt.plot(x[1])