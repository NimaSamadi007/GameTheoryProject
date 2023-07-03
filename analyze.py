import numpy as np
import csv
import matplotlib.pyplot as plt

# Read results:
print("Input results path: ", end="")
path = input()

results = []
with open(f"{path}/results.csv", "r") as f:
    reader = csv.DictReader(f)
    for item in reader:
        results.append(dict(item))

avg_surgery_cost = []
avg_surgery_time = []
avg_compl_time = []
rate_in = []
rate_out = []
stability = []

for res in results:
    avg_surgery_cost.append(np.fromstring(res['avg_surgery_cost'][1:-1], sep=' '))
    avg_surgery_time.append(np.fromstring(res['avg_surgery_time'][1:-1], sep=' '))
    avg_compl_time.append(np.fromstring(res['avg_compl_time'][1:-1], sep=' '))
    rate_in.append(float(res['rate_in']))
    rate_out.append(float(res['rate_out']))
    stability.append(res['stability'])

N = len(results)
avg_surgery_cost = np.array(avg_surgery_cost)
avg_surgery_time = np.array(avg_surgery_time)
avg_compl_time = np.array(avg_compl_time)

plt.figure()
plt.plot(np.arange(1, N+1), avg_surgery_cost[:, 0], label="Averge surgery A cost")
plt.plot(np.arange(1, N+1), avg_surgery_cost[:, 1], label="Averge surgery B cost")
plt.plot(np.arange(1, N+1), avg_surgery_cost[:, 2], label="Averge surgery C cost")
plt.xlabel("Run number")
plt.ylabel("Cost")
plt.title("Average surgery cost")
plt.legend()
plt.grid(True)
plt.savefig(f"results/{path}_avg_surgery_cost.png")
print("Average surgery cost in total: ")
print(np.mean(avg_surgery_cost, axis=0))

plt.figure()
plt.plot(np.arange(1, N+1), avg_surgery_time[:, 0], label="Averge surgery A time")
plt.plot(np.arange(1, N+1), avg_surgery_time[:, 1], label="Averge surgery B time")
plt.plot(np.arange(1, N+1), avg_surgery_time[:, 2], label="Averge surgery C time")
plt.xlabel("Run number")
plt.ylabel("Time")
plt.title("Average surgery time")
plt.legend()
plt.grid(True)
plt.savefig(f"results/{path}_avg_surgery_time.png")
print("Average surgery time in total: ")
print(np.mean(avg_surgery_time, axis=0))

plt.figure()
plt.plot(np.arange(1, N+1), avg_compl_time[:, 0], label="Averge surgery A completion time")
plt.plot(np.arange(1, N+1), avg_compl_time[:, 1], label="Averge surgery B completion time")
plt.plot(np.arange(1, N+1), avg_compl_time[:, 2], label="Averge surgery C completion time")
plt.xlabel("Run number")
plt.ylabel("Time")
plt.title("Average surgery completion time")
plt.legend()
plt.grid(True)
plt.savefig(f"results/{path}_avg_compl_time.png")
print("Average completion time in total: ")
print(np.mean(avg_compl_time, axis=0))

plt.figure()
plt.plot(np.arange(1, N+1), rate_in, label="Input rate")
plt.plot(np.arange(1, N+1), rate_out, label="Output rate")
plt.xlabel("Run number")
plt.ylabel("Rate")
plt.title("Input/output rate")
plt.legend()
plt.grid(True)
plt.savefig(f"results/{path}_IO_rate.png")
print("Average rate: ")
print(f"Input rate: {np.mean(rate_in):.3f}, output rate: {np.mean(rate_out):.3f}")

print(f"Queue stabilities:\n{stability}")
