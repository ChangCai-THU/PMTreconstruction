import numpy as np

#从一个peak，筛选出对应的records
def peak_records_selection(records,peak):
    #firstly findout the start and end time of the peaklet
    start, end = peak['time'],peak['time']+peak['length']*peak['dt']
    dt = 10
    #secondly find out the records in this interval,
    #If a peak starts between peakstart and peakend, or if it starts before peakstart but end after peakstart
    sequence = (records[:]['time']<end) * (records[:]['time'] > start) + (records[:]['time'] < start * (records[:]['time'] + 10*records[:]['length'] > start))
    records_in_peak = records[sequence]
    return records_in_peak

#从一个events_info，筛选出对应的records
def event_records_selection(records,event):
    #firstly findout the start and end time of the peaklet
    S1_start, S1_end = event['s1_time'],event['s1_endtime']
    S2_start, S2_end = event['s2_time'],event['s2_endtime']
    dt = 10
    #secondly find out the records in this interval,
    #If a peak starts between start and end, or if it starts before peakstart but end after peakstart
    S1sequence = (records[:]['time']<S1_end) * (records[:]['time'] > S1_start) + (records[:]['time'] < S1_start * ((records[:]['time'] + 10*records[:]['length']) > S1_start))
    S1records_in_peak = records[S1sequence]
    S2sequence = (records[:]['time']<S2_end) * (records[:]['time'] > S2_start) + (records[:]['time'] < S2_start * ((records[:]['time'] + 10*records[:]['length']) > S2_start))
    S2records_in_peak = records[S2sequence]
    return S1records_in_peak, [S1_start, S1_end], S2records_in_peak, [S2_start, S2_end]

#从一段时间内所有的channel的records中，对于不同channel的records data进行拼接
def channelrecord(records,channel,start,end):
    #given all the records belong to the same peak, 
    #return the data from peak start to peak end, with records data on it
    #Firstly select the records belong to the same channel
    channelrecords = records[records['channel']==channel]
    #Then make the empty data array from peak start to peak end
    peaklength = int((end-start)/10)
    data = np.zeros(peaklength)
    for partrecord in channelrecords:
        index = int((partrecord['time']-start)/10)
        length = partrecord['length']
        #print(index,length,partrecord['data'])
        #print('****',end-partrecord['time'])
        if index<0:
            if peaklength >= length+index:
                data[:length+index]+=partrecord['data'][-index:length]
            else:
                data+=partrecord['data'][-index:peaklength-index]
        else:
            try:
                data[index:index+length]+=partrecord['data'][:length]
            except ValueError:
                recordzerolength = int((end-partrecord['time'])/10)
                data[index:]+=partrecord['data'][:recordzerolength]
    return data

#对于某一个channel的recordsdata，进行ADC counts到光子数的转化，目前仅是将前者除以gain，实际做SPE shape的解卷积更为合理,直接将topemap导入，避免每个通道调用程序时重复载入
# gainrun="021445"
# print("Will use gains from run {:s}".format(gainrun))
# cmt=straxen.CorrectionsManagementServices()
# my_fav_gains = cmt.get_pmt_gains(gainrun,'to_pe_model','ONLINE') #this would give you the actual gains 
def adc_to_pe(data,channel,topemap):
    return data*topemap[channel]

#给定所有的records，对channellist中的每个通道，计算出对应的PE data，进行求和，如果channellist为所有的不饱和通道，则return结果为所有不饱和通道的PE波形之和。
def sumrecords(records,channellist,start,end,topemap):
    sumdata = np.zeros(int((end-start)/10))
    for channel in channellist:
        data = channelrecord(records,channel,start,end)
        sumdata+=adc_to_pe(data,channel,topemap)
    return sumdata


def satpoint(channeldata,template):
    #给定一个通道的ADC data，判断饱和点，即饱和点之前的可以作为参考波形进行重建。若没有饱和，则return None
    satpart = np.where(channeldata>14400)[0]
    if len(satpart)>0:
        return satpart[0]
    else:
        return None
