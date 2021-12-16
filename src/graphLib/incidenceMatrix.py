class IncidenceMatrix:
    rows = []
    columns = []
    values = [[]]
    def __init__(self,rows=[],columns=[],defaultValue=0) -> None:
        self.rows       = rows
        self.columns    = columns

        for r in rows:
            filledRow = []
            for c in columns:
                filledRow.append(defaultValue)
            self.values.append(filledRow)
                

    def addRow(self,row,defaultValue=0):
        self.rows.append(row)
        self.values.append(defaultValue for c in self.columns)

    def deleteRow(self,row):
        index = self.rows.find(row)
        del self.rows[index]
        del self.values[index]

    def addColumn(self,column,defaultValue=0):
        self.columns.append(column)
        for r in range(0,len(self.rows)):
            self.rows[r].append(defaultValue)

    def deleteColumn(self,column):
        index = self.columns.find(column)
        del self.columns[index]
        for r in range(0,len(self.rows)):
            del self.rows[r][column]

    def setValue(self,row,column,value):
        self.values[row][column] = value
    
    def getValue(self,row,column):
        return self.values[row][column]

    def changeValue(self,row,column,func):
        self.values[row][column] = func(self.values[row][column])

    def addValue(self,row,column,value=1):
        self.changeValue(row,column,lambda x: x+value)

    def getRow(self,row):
        index = self.rows.find(row)
        return self.rows[index]

    def getColumn(self,column):
        index = self.columns.find(column)
        columnValues = []
        for r in self.rows:
            columnValues.append(r[index])
        return columnValues