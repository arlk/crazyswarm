#!/usr/bin/env python

import numpy as np
import rospy
from crazyflie_driver.msg import GenericLogData
import csv

from pycrazyswarm import *
import uav_trajectory

from yaml import load, Loader

def callback(data):
  with open('log.csv', mode='a') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=',')
      csv_writer.writerow(data.values)

if __name__ == "__main__":
    open('log.csv', 'w').close()

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    # load params
    params = load(file('log.yaml', 'rb'), Loader=Loader)
    for cf in allcfs.crazyflies:
        for k in params:
            cf.setParam("ctrlL1/" + k, params[k])

    rospy.Subscriber("/cf1/log1", GenericLogData, callback)

    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv("figure8.csv")

    for cf in allcfs.crazyflies:
        cf.uploadTrajectory(0, 0, traj1)

    allcfs.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.5)
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
        cf.goTo(pos, 0, 2.0)
    timeHelper.sleep(2.5)

    allcfs.startTrajectory(0, timescale=1.0)
    timeHelper.sleep(traj1.duration * 1.0 + 2.0)
    #  allcfs.startTrajectory(0, timescale=0.75, reverse=True)
    #  timeHelper.sleep(traj1.duration * 0.75 + 2.0)

    allcfs.land(targetHeight=0.06, duration=2.0)
    timeHelper.sleep(3.0)

    # cost fn:
    with open('log.csv', mode='rb') as csv_file:
        reader = csv.reader(csv_file)
        count = 0
        cost = 0.0
        for row in reader:
            cost += float(row[0]) + 0.5*float(row[1]) + float(row[2])
            count += 1

    print("Cost: ", 100*cost/count)
