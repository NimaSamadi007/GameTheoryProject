import numpy as np
from hospital import Hospital
from surgery import Surgery
from utils import *
from log import LogType
import csv
from __init__ import logger

DA_phase = 0

def initParams(num_slots, rate_coef, waiting_slot):
    # np.random.seed(42)

    # Create hospitals:
    hosp_a = Hospital(0, np.array([2, 5, 7])) # 0 -> 'a'
    hosp_b = Hospital(1, np.array([7, 2, 5])) # 1 -> 'b'
    hosp_c = Hospital(2, np.array([5, 7, 2])) # 2 -> 'c'
    hospitals = [hosp_a, hosp_b, hosp_c]

    # Create all requests and their queue:
    reqs = genRequests(num_slots, rate_coef)
    all_surgs = createSurgeries(reqs, waiting_slot)
    surg_queue = createQueue(all_surgs)

    return hospitals, surg_queue

def selectRequests(hospitals, queue, timestamp):
    current_surgs = []
    index = 0
    # Either 3 requests have been selected or we are in the current slot
    while index < len(queue) and \
          len(current_surgs) < 3 and \
          queue[index].creation_time <= timestamp + 8:
        # check whether surgery participates or not
        opt_hosp = queue[index].proposeOptimal()
        if opt_hosp is None:
            # Must participate
            current_surgs.append(queue[index])
        else:
            # Check whether optimal hospital is empty
            if hospitals[opt_hosp].empty:
                # Then participate
                current_surgs.append(queue[index])
            else:
                # Reduce waiting slot and wait
                queue[index].waiting_slot -= 1
        index += 1

    return current_surgs, index

def emptyFinshedHospitals(hosps):
    for hosp in hosps:
        if not hosp.empty:
            hosp.remain_time -= 8 # hours has elapsed
        if hosp.remain_time <= 0: # This surgery is finished
            hosp.clear()

def runDA(current_surgs, hospitals):
    global DA_phase
    if DA_phase % 250 == 0:
        logger.log(f"At DA {DA_phase}", log_type=LogType.INFO)
    DA_phase += 1

    all_assigned = isAllAssigned(current_surgs)
    all_full = isAllFull(hospitals)
    no_proposal = False
    logger.log(f"Before: all assigned: {all_assigned}, all_full: {all_full}")
    while not all_assigned and not all_full and not no_proposal:
        for surg in current_surgs:
            if not surg.assigned:
                proposal = surg.propose()
                logger.log(f"Surg: {surg}")
                logger.log(f"Proposal: {proposal}")
                if proposal is None:
                    # No available hospitals - run out of proposals
                    no_proposal = True
                    break
                status = hospitals[proposal].evaluate(surg)
                logger.log(f"Status: {status}")
                if status:
                    hospitals[proposal].assign(surg)
        all_assigned = isAllAssigned(current_surgs)
        all_full = isAllFull(hospitals)
    return

def calRequestRate(surgs: list[Surgery]) -> tuple[float]:
    logger.log(25*"=", log_type=LogType.INFO)
    logger.log("Rates:", log_type=LogType.INFO)    
    max_in_surg = max(surgs, key=lambda surg: surg.creation_time)
    max_out_surg = max(surgs, key=lambda surg: surg.serve_time+surg.creation_time)
    max_in_time = max_in_surg.creation_time
    max_out_time = max_out_surg.creation_time+max_out_surg.serve_time
    num_surgs = len(surgs)
    return num_surgs/max_in_time, num_surgs/max_out_time

def main(num_slots, rate_coef, waiting_slot):
    # initalize algorithm
    timestamp = 0
    completed_surg = []
    hospitals, surg_queue = initParams(num_slots, rate_coef, waiting_slot)

    # Run algorithm:
    while len(surg_queue):
        logger.log(f"At ts: {timestamp}")
        logger.log(f"Surgery queue: {surg_queue}")
        # Empty finished hospitals:
        emptyFinshedHospitals(hospitals)

        current_surgs, index = selectRequests(hospitals, surg_queue, timestamp)

        logger.log("Current surgeries: ", end="")
        for tmp in current_surgs:
            logger.log(f"{tmp}, ", end="")

        logger.log(f"\nRemain time: {hospitals[0].remain_time}, {hospitals[1].remain_time}, {hospitals[2].remain_time}")

        # Perform DA (surgeries propose to hospitals)
        runDA(current_surgs, hospitals)

        logger.log(25*"=")
        # Accept requests now:
        for surg in current_surgs:
            if surg.assigned:
                # Hospital related attributes
                hosp = surg.matched_hospital
                hosp.empty = False
                time_offset = surg.creation_time-timestamp
                hosp.remain_time = surg.all_surg_time[hosp.hosp_type]+time_offset*(time_offset > 0)
                hosp.num_surg[surg.surg_type] += 1
                hosp.surg_time[surg.surg_type] += surg.all_surg_time[hosp.hosp_type]
                hosp.revenue[surg.surg_type] += hosp.pref[surg.surg_type]

                # Surgery related attributes
                dt = timestamp-surg.creation_time
                surg.serve_time = dt*(dt>0)
                surg.compl_time = surg.all_surg_time[hosp.hosp_type] + surg.serve_time

                logger.log(f"{surg} matched with {surg.matched_hospital}")

                for j in range(index):
                    if surg_queue[j].ID == surg.ID:
                        completed_surg.append(surg_queue.pop(j))
                        break
            else:
                # Reset proposals:
                surg.proposed = [False, False, False]

        timestamp += 8
        logger.log(50*"=")


    avg_surgery_cost, avg_surgery_time = showMetrics(hospitals)
    avg_compl_time = showSurgeryStatus(completed_surg)

    rate_in, rate_out = calRequestRate(completed_surg)
    logger.log(f"Input rate: {rate_in:.3f}, output rate: {rate_out:.3f}", log_type=LogType.INFO)
    if rate_in > rate_out:
        logger.log("Queue is unstable on average", log_type=LogType.INFO)
    else:
        logger.log("Queue is stable on average", log_type=LogType.INFO)

    results = {'avg_surgery_cost': avg_surgery_cost,
               'avg_surgery_time': avg_surgery_time,
               'avg_compl_time': np.array(avg_compl_time),
               'rate_in': rate_in,
               'rate_out': rate_out,
               'stability': not(rate_in > rate_out)}

    return results

if __name__ == "__main__":
    all_results = []
    print("Enter N: ", end="")
    N = int(input())
    print("Enter num_slots: ", end="")
    num_slots = int(input())
    print("Enter rate_conf: ", end="")
    rate_coef = float(input())
    print("Enter K: ", end="")
    waiting_slots = int(input())

    for i in range(N):
        DA_phase = 0
        logger.log(100*"-", log_type=LogType.INFO)
        logger.log(f"At run {i}:", log_type=LogType.INFO)
        results = main(num_slots, rate_coef, waiting_slots)
        all_results.append(results)

    # Write to file
    with open('results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)
    
    print("Results saved!")
