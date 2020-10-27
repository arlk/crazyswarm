#!/usr/bin/env python

import numpy as np

from pycrazyswarm import *
import uav_trajectory

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv("figure8.csv")

    for cf in allcfs.crazyflies:
        cf.setParam("ctrlL1/l1on", 0)
        cf.uploadTrajectory(0, 0, traj1)

    allcfs.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.5)
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
        cf.goTo(pos, 0, 2.0)
    timeHelper.sleep(2.5)

    allcfs.startTrajectory(0, timescale=1.0)
    timeHelper.sleep(traj1.duration * 1.0 + 2.0)
    #  allcfs.startTrajectory(0, timescale=0.8, reverse=True)
    #  timeHelper.sleep(traj1.duration * 0.8 + 2.0)

    allcfs.land(targetHeight=0.06, duration=2.0)
    timeHelper.sleep(3.0)

    #  for cf in allcfs.crazyflies:
    #      cf.setParam("ctrlL1/l1on", 2)
    #      cf.uploadTrajectory(0, 0, traj1)
    #
    #  allcfs.takeoff(targetHeight=1.0, duration=2.0)
    #  timeHelper.sleep(2.5)
    #  for cf in allcfs.crazyflies:
    #      pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
    #      cf.goTo(pos, 0, 2.0)
    #  timeHelper.sleep(2.5)
    #
    #  allcfs.startTrajectory(0, timescale=1.0)
    #  timeHelper.sleep(traj1.duration * 1.0 + 2.0)
    #  allcfs.startTrajectory(0, timescale=0.8, reverse=True)
    #  timeHelper.sleep(traj1.duration * 0.8 + 2.0)
    #
    #  allcfs.land(targetHeight=0.06, duration=2.0)
    #  timeHelper.sleep(3.0)

