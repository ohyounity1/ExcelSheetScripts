from dataclasses import dataclass
from dataclasses import field

@dataclass
class TreeProperty:
	Name: str
	Children: list = field(default_factory=list)
	ValueOnNextLevel: bool = False

def ErrorListToTreeDisplay(objects, properties, config=None, dataConverter=None):
	indentLevel = 2
	levelMarker = '-' * indentLevel
	if(config is not None):
		indentLevel = config.IndentLevel
		levelMarker = config.LevelMarker * indentLevel

	for o in objects:
		currentLevel = properties
		previousLevels = []
		currentLevelMarker = ''
		maxPropertyIndex = len(currentLevel)
		index = 0
		while(index < maxPropertyIndex):
			p = currentLevel[index]
			propValue = getattr(o, p.Name)
			if(dataConverter is not None):
				propValue = dataConverter(p.Name, propValue)
			if(p.ValueOnNextLevel):
				print(f'{currentLevelMarker}{p.Name}:\n{currentLevelMarker + levelMarker}{propValue}')
			else:
				print(f'{currentLevelMarker}{p.Name}:{propValue}')
			index += 1
			if(len(p.Children) > 0):
				unfinishedPreviousLevelProperties = list()
				for iindex in range(index, len(currentLevel)):
					unfinishedPreviousLevelProperties.append(currentLevel[iindex])
				if(len(unfinishedPreviousLevelProperties) > 0):
					previousLevels.append(unfinishedPreviousLevelProperties)
				index = 0
				currentLevel = p.Children
				currentLevelMarker += levelMarker
				maxPropertyIndex = len(currentLevel)
			elif(index == maxPropertyIndex):
				if(len(previousLevels) > 0):

					currentLevel = previousLevels.pop()
					index = 0
					maxPropertyIndex = len(currentLevel)
					currentLevelMarker = currentLevelMarker[:-markersPerLevel]