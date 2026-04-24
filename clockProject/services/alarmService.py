"""Service layer for alarm management."""

from __future__ import annotations

from datetime import time
from typing import Optional

from dataStructures.doublyCircularList import DoublyCircularList
from models.alarm import Alarm


class AlarmService:
    """Manages alarms and alarm navigation with a circular list."""

    def __init__(self) -> None:
        self._nextAlarmId = 1
        self.alarms: list[Alarm] = []
        self.alarmNavigation: DoublyCircularList[Alarm] = DoublyCircularList()

    def createAlarm(self, label: str, alarmTime: time, repeatDaily: bool = False) -> Alarm:
        """Create and register a new alarm."""
        alarm = Alarm(
            alarmId=self._nextAlarmId,
            label=label,
            alarmTime=alarmTime,
            enabled=True,
            repeatDaily=repeatDaily,
        )
        self._nextAlarmId += 1

        self.alarms.append(alarm)
        self.alarmNavigation.append(alarm)
        return alarm

    def removeAlarm(self, alarmId: int) -> bool:
        """Remove an alarm by id from list and navigation structure."""
        alarm = self.findAlarmById(alarmId)
        if alarm is None:
            return False

        self.alarms.remove(alarm)
        self.alarmNavigation.remove(alarm)
        return True

    def findAlarmById(self, alarmId: int) -> Optional[Alarm]:
        """Find an alarm by id."""
        for alarm in self.alarms:
            if alarm.alarmId == alarmId:
                return alarm
        return None

    def getEnabledAlarms(self) -> list[Alarm]:
        """Return only active alarms."""
        return [alarm for alarm in self.alarms if alarm.enabled]

    def moveToNextAlarm(self) -> Optional[Alarm]:
        """Move navigation cursor to next alarm."""
        return self.alarmNavigation.moveNext()

    def moveToPreviousAlarm(self) -> Optional[Alarm]:
        """Move navigation cursor to previous alarm."""
        return self.alarmNavigation.movePrevious()

    def getCurrentAlarm(self) -> Optional[Alarm]:
        """Return current alarm from navigation cursor."""
        return self.alarmNavigation.getCurrent()

    def checkDueAlarms(self, currentTime: time) -> list[Alarm]:
        """Return alarms that should ring for the provided time."""
        dueAlarms: list[Alarm] = []
        for alarm in self.getEnabledAlarms():
            if alarm.alarmTime.hour == currentTime.hour and alarm.alarmTime.minute == currentTime.minute:
                dueAlarms.append(alarm)
        return dueAlarms
