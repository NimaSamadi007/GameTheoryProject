import numpy as np
from surgery import Surgery
from log import LogType
from __init__ import logger

def genNumRequests(num_slots, rate_coef):
    A_num_req = np.random.poisson(0.2*8*rate_coef, num_slots)
    B_num_req = np.random.poisson(0.1*8*rate_coef, num_slots)
    C_num_req = np.random.poisson(0.05*8*rate_coef, num_slots)
    return np.sum(A_num_req), np.sum(B_num_req), np.sum(C_num_req)

def genRequests(num_slots, rate_coef):
    A_rate, B_rate, C_rate = 0.2*rate_coef, \
                             0.1*rate_coef, \
                             0.05*rate_coef

    num_A, num_B, num_C = genNumRequests(num_slots, rate_coef)
    logger.log(f"Generated {num_A}, {num_B}, and {num_C} of A, B, C requests", log_type=LogType.INFO)

    A_reqs = np.random.exponential(1/A_rate, num_A)
    B_reqs = np.random.exponential(1/B_rate, num_B)
    C_reqs = np.random.exponential(1/C_rate, num_C)
    
    return {"A": np.cumsum(A_reqs),
            "B": np.cumsum(B_reqs),
            "C": np.cumsum(C_reqs)}

def genSurgeryTime(surg_rate, avg_surg_time):
    return np.random.exponential(avg_surg_time)/surg_rate
    # return avg_surg_time/surg_rate

def createSurgeries(reqs):
    surgs = {}
    A_surg_rate = np.array([1, 1/2, 1/3])
    B_surg_rate = np.array([1/3, 1, 1/2])
    C_surg_rate = np.array([1/2, 1/3, 1])
    
    tmp_surg = []
    for i in range(len(reqs['A'])):
        A_surg_time = genSurgeryTime(A_surg_rate, 2)
        tmp_surg.append(Surgery(0, reqs['A'][i], A_surg_time))
    surgs['A'] = tmp_surg

    tmp_surg = []
    for i in range(len(reqs['B'])):
        B_surg_time = genSurgeryTime(B_surg_rate, 5)
        tmp_surg.append(Surgery(1, reqs['B'][i], B_surg_time))
    surgs['B'] = tmp_surg

    tmp_surg = []
    for i in range(len(reqs['C'])):
        C_surg_time = genSurgeryTime(C_surg_rate, 10)
        tmp_surg.append(Surgery(2, reqs['C'][i], C_surg_time))
    surgs['C'] = tmp_surg
    
    return surgs

def createQueue(surgs):
    queue = surgs['A']
    queue.extend(surgs['B'])
    queue.extend(surgs['C'])
    # Sort queue based on the arrival time
    queue.sort(key=lambda surg: surg.creation_time)
    return queue

def isAllAssigned(surgs):
    assigned = True
    for surg in surgs:
        assigned = assigned and surg.assigned
    return assigned

def isAllFull(hosps):
    full = True
    for hosp in hosps:
        full = full and (not hosp.empty)
    return full

def showMetrics(hosps: list) -> None:
    logger.log(25*"=", log_type=LogType.INFO)
    logger.log("Required metrics:", log_type=LogType.INFO)
    logger.log(f"Number of surgeries: {hosps[0].num_surg}, {hosps[1].num_surg}, {hosps[2].num_surg}")

    surgery_num_matrix = np.stack([hosps[0].num_surg,
                                   hosps[1].num_surg,
                                   hosps[2].num_surg], axis=1)
    surgery_num = np.sum(surgery_num_matrix, axis=1)
    cost_matrix = np.stack([hosps[0].revenue,
                            hosps[1].revenue,
                            hosps[2].revenue], axis=1)
    avg_surgery_cost = np.sum(cost_matrix, axis=1)/surgery_num
    surgery_time_matrix = np.stack([hosps[0].surg_time,
                                    hosps[1].surg_time,
                                    hosps[2].surg_time], axis=1)
    avg_surgery_time = np.sum(surgery_time_matrix, axis=1)/surgery_num

    logger.log(f"Average cost (per surgery):"
               f" A: {avg_surgery_cost[0]:.3f},"
               f" B: {avg_surgery_cost[1]:.3f},"
               f" C: {avg_surgery_cost[2]:.3f}", 
               log_type=LogType.INFO)
    logger.log(f"Average surgery time:"
               f" A: {avg_surgery_time[0]:.3f},"
               f" B: {avg_surgery_time[1]:.3f},"
               f" C: {avg_surgery_time[2]:.3f}", 
               log_type=LogType.INFO)

    return avg_surgery_cost, avg_surgery_time

def showSurgeryStatus(surgs: list) -> None:
    A_compl_time = []
    B_compl_time = []
    C_compl_time = []

    logger.log(25*"=", log_type=LogType.INFO)
    logger.log("Surgery status:")
    COL_NUM = 3
    for i in range(COL_NUM, len(surgs), COL_NUM):
        for j in range(i-COL_NUM, i):
            logger.log(f"{surgs[j]}:{surgs[j].compl_time}", ", ")
        logger.log("")
    for j in range(i, len(surgs)):
        logger.log(f"{surgs[j]}:{surgs[j].compl_time}", ", ")
    logger.log("")

    for surg in surgs:
        if surg.surg_type == 0:
            A_compl_time.append(surg.compl_time)
        elif surg.surg_type == 1:
            B_compl_time.append(surg.compl_time)
        else:
            C_compl_time.append(surg.compl_time)

    avg_compl_time = [np.mean(A_compl_time),
                      np.mean(B_compl_time),
                      np.mean(C_compl_time)]
    logger.log(f"Average completion time (per surgery):"
               f" A: {avg_compl_time[0]:.3f},"
               f" B: {avg_compl_time[1]:.3f},"
               f" C: {avg_compl_time[2]:.3f}", 
               log_type=LogType.INFO)

    return avg_compl_time
