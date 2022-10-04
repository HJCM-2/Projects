import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
for i in range(20):
	if i % 1 == 0:
		v = np.load("./data_test/speed_v%s.npy"%(i))
		w = np.load("./data_test/speed_w%s.npy"%(i))
		# print(v,w)
		n = range(len(w))
		# plt.figure(figsize=(7,5))
		plt.subplot(211)
		plt.plot(n, v, lw=1.5, label = 'v%s'%(i))
		plt.grid(True)
		plt.legend(loc = 0)  # auto illustration
		plt.xlim(0,100)
		plt.ylim(-0.01,0.6)
		plt.xlabel('step')
		# plt.ylabel('v%s'%(i))
		plt.ylabel('v')
		plt.title('speed%s'%(i))
		
		plt.subplot(212)
		plt.plot(n, w, 'g', lw=1.5, label = 'w%s'%(i))
		plt.grid(True)
		plt.legend(loc = 0)  # auto illustration
		plt.xlim(0,100)
		plt.ylim(-0.1-np.pi/2,0.1+np.pi/2)
		plt.xlabel('step')
		# plt.ylabel('w%s'%(i))
		plt.ylabel('w')
		plt.savefig("./picture_test/speed%s.jpg"%(i))
		# plt.show()
		plt.clf()
		plt.close("./picture_test/speed%s.jpg"%(i))
print("Picture is on the picture_test now!")
