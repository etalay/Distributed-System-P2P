import numpy

import matplotlib.pyplot as plt

#iki diziyi olusturup onlari tam sayi degerlerine yuvarladik.

first_series =  numpy.random.normal(5,1.5,10000) 

first_series_arounded = numpy.around(first_series)

second_series =  numpy.random.normal(-5,1.5,10000)

second_series_arounded = numpy.around(second_series)

counter_index = 0 #İki histogram arasindaki farki bulurken histogramlarin elemanları arasinda çıkarma işlemi yapmak için kullaniyoruz

first_histogram = [0.0 for i in range(40)]

second_histogram = [0.0 for i in range(40)]

#Asagidaki for donguleriyle histogrami olusturup eslesen degerleri arttirdik.

for i in range(0,9999):
	
	first_histogram[int(first_series_arounded[i])+20] = first_histogram[int(first_series_arounded[i])+20] + 1

for j in range(0,9999):
	
	second_histogram[int(second_series_arounded[j])+20] = second_histogram[int(second_series_arounded[j])+20] + 1

#Burada da olusturdugumuz histogramlari normalize ettik.

for x in range(0,39):
	first_histogram[x] = first_histogram[x]/10000 

for y in range(0,39):
	second_histogram[y] = second_histogram[y]/10000



print(first_histogram)
print(" ")
print(second_histogram)

#İki histogram arasindaki mesafeyi bulabilmek icin 0'dan farkli elemanlarin indislerini buldum.
first_not_zero_list = []
second_not_zero_list = []

for i in range(0,39):
    if(first_histogram[i] != 0 ):
        (first_not_zero_list).append(i)
        
for j in range(0,39):
    if(second_histogram[j] != 0 ):
        (second_not_zero_list).append(j)




#Distance'i bulabilmek için en yakin elemanlar arasinda işlem yapmaya çaliştim ama bitiremedim
'''
D=0

len(first_not_zero_list) = size_of_fnzl

for counter_index in range(0,size_of_fnzl): 
if(first_histogram[first_not_zero_list[counter_index]]> second_histogram[second_not_zero_list[counter_index]]):
    (first_not_zero_list-second_not_zero_list)*(first_histogram[first_not_zero_list[counter_index]]-second_histogram[second_not_zero_list[counter_index]])=D

for counter_index in range(0,size_of_fnzl): 
if(first_histogram[first_not_zero_list[counter_index]]< second_histogram[second_not_zero_list[counter_index]]):
     (first_not_zero_list-second_not_zero_list)*second_histogram[second_not_zero_list[counter_index]]-first_histogram[first_not_zero_list[counter_index]]=D    

'''        
print(first_not_zero_list)

print(second_not_zero_list)

bins = numpy.linspace(-20, 20)
plt.hist(first_series, bins, histtype='stepfilled', normed=True, color='b', label='First Histogram')
plt.hist(second_series, bins, histtype='stepfilled', normed=True, color='r', alpha=0.5, label='Second Histogram')
plt.title("first/Second Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.legend()
plt.show()



