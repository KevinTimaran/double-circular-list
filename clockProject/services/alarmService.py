"""Service layer for alarm management."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from dataStructures.doublyCircularList import DoublyCircularList
from models.alarm import Alarm


class AlarmService:
    """Manages alarms and alarm navigation with a circular list."""

    def __init__(self) -> None:
        self._nextAlarmId = 1
        self.alarmNavigation: DoublyCircularList[Alarm] = DoublyCircularList()
        self._lastTriggeredMinuteByAlarmId: dict[int, str] = {}

    def addAlarm(self, alarm: Alarm) -> Alarm:
        """Add an alarm to the circular list and assign an id if needed."""
        alarmId = alarm.alarmId if alarm.alarmId > 0 else self._nextAlarmId

        storedAlarm = Alarm(
            alarmId=alarmId,
            hour=alarm.hour,
            minute=alarm.minute,
            label=alarm.label,
            enabled=alarm.enabled,
        )

        if alarmId >= self._nextAlarmId:
            self._nextAlarmId = alarmId + 1

        self.alarmNavigation.append(storedAlarm)
        return storedAlarm

    def updateAlarm(self, alarmId: int, updatedAlarm: Alarm) -> bool:
        """Update an existing alarm by id."""
        existingAlarm = self.findAlarmById(alarmId)
        if existingAlarm is None:
            return False

        existingAlarm.hour = updatedAlarm.hour
        existingAlarm.minute = updatedAlarm.minute
        existingAlarm.label = updatedAlarm.label
        existingAlarm.enabled = updatedAlarm.enabled
        return True

    def removeAlarm(self, alarmId: int) -> bool:
        """Remove an alarm by id from the circular list."""
        alarm = self.findAlarmById(alarmId)
        if alarm is None:
            return False

        self.alarmNavigation.remove(alarm)
        self._lastTriggeredMinuteByAlarmId.pop(alarmId, None)
        return True

    def toggleAlarm(self, alarmId: int) -> bool:
        """Toggle the enabled state of an alarm."""
        alarm = self.findAlarmById(alarmId)
        if alarm is None:
            return False

        alarm.enabled = not alarm.enabled
        return True

    def findAlarmById(self, alarmId: int) -> Optional[Alarm]:
        """Find an alarm by id."""
        for alarm in self.alarmNavigation:
            if alarm.alarmId == alarmId:
                return alarm
        return None

    def getAllAlarms(self) -> list[Alarm]:
        """Return all alarms in their current navigation order."""
        return list(self.alarmNavigation)

    def getCurrentAlarm(self) -> Optional[Alarm]:
        """Return the alarm currently selected by the circular cursor."""
        return self.alarmNavigation.getCurrent()

    def moveNextAlarm(self) -> Optional[Alarm]:
        """Move navigation cursor to the next alarm."""
        return self.alarmNavigation.moveNext()

    def movePreviousAlarm(self) -> Optional[Alarm]:
        """Move navigation cursor to the previous alarm."""
        return self.alarmNavigation.movePrevious()

    def checkTriggeredAlarms(self, currentDateTime: datetime) -> list[Alarm]:
        """Return alarms that should trigger for the provided date/time."""
        currentMinuteKey = currentDateTime.strftime("%Y%m%d%H%M")
        triggeredAlarms: list[Alarm] = []

        for alarm in self.alarmNavigation:
            if not alarm.enabled:
                continue

            if alarm.hour != currentDateTime.hour or alarm.minute != currentDateTime.minute:
                continue

            if self._lastTriggeredMinuteByAlarmId.get(alarm.alarmId) == currentMinuteKey:
                continue

            self._lastTriggeredMinuteByAlarmId[alarm.alarmId] = currentMinuteKey
            triggeredAlarms.append(alarm)

        return triggeredAlarms
