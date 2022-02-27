class Table:

    def __init__(self,) -> None:
        self.rows = []
        self.columns = []
        self.values = []

    @classmethod
    def withColumnsAndRows(cls,rows,columns):
        obj = cls()
        for row in rows:
            obj.addRow(row)
        for column in columns:
            obj.addColumn(column)
        return obj

    @classmethod
    def withColumnsAndRowsAndValues(cls,rows,columns,values):
        obj = cls()
        for row in rows:
            obj.addRow(row)
        for column in columns:
            obj.addColumn(column)
        obj.values = values
        return obj
        
                
    # Adds a row to the Table
    # rowName -> name of the row
    def addRow(self,rowName,defaultValue=0):
        self.rows.append(rowName)
        self.values.append([defaultValue for c in self.columns])

    # rowName -> name of the row
    def deleteRow(self,rowName):
        index = self.rows.index(rowName)
        del self.rows[index]
        del self.values[index]

    def addColumn(self,columnName,defaultValue=0):
        self.columns.append(columnName)
        for r in range(0,len(self.rows)):
            self.values[r].append(defaultValue)

    def deleteColumn(self,columnName):
        index = self.columns.index(columnName)
        del self.columns[index]
        for r in range(0,len(self.rows)):
            del self.values[r][index]

    def setColumn(self,columnName,value):
        columnIndex = self.columns.index(columnName)
        for rowIndex in range(0,len(self.values)):
            self.values[rowIndex][columnIndex] = value

    def changeRowByIndex(self,rowIndex,func):
        for columnIndex in range(0,len(self.columns)):
            self.values[rowIndex][columnIndex] = func(self.values[rowIndex][columnIndex],self.columns[columnIndex])
            

    def setValue(self,rowName,columnName,value):
        rowIndex = self.rows.index(rowName)
        columnIndex = self.columns.index(columnName)
        self.values[rowIndex][columnIndex] = value
    
    def getValue(self,rowName,columnName):
        rowIndex = self.rows.index(rowName)
        columnIndex = self.columns.index(columnName)
        return self.values[rowIndex][columnIndex]

    def findInRow(self,rowName,value):
        row = self.getRow(rowName)
        for column in self.columns:
            index = self.columns.index(column)
            if row[index] == value:
                return column

    def changeValue(self,rowName,columnName,func):
        rowIndex = self.rows.index(rowName)
        columnIndex = self.columns.index(columnName)
        self.values[rowIndex][columnIndex] = func(self.values[rowIndex][columnIndex])

    def addValue(self,rowName,columnName,value=1):
        self.changeValue(rowName,columnName,lambda x: x+value)

    def getRow(self,rowName):
        index = self.rows.index(rowName)
        return self.values[index]

    def getColumn(self,columnName):
        index = self.columns.index(columnName)
        columnValues = []
        for r in self.values:
            columnValues.append(r[index])
        return columnValues

    def __str__(self):
        text = "   |"
        for c in self.columns:
            text += str(c) + "|"
        text += "\n\n"
        for r in range(0,len(self.rows)):
            text += str(self.rows[r]) + "  "
            for x in self.values[r]:
                text += "|" + str(x)
            text += "\n"
        return text
