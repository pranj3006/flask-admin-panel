from extensions import db

class BaseRepository:
    def __init__(self,model=None,res=None,db=db) -> None:
        self.model=model
        self.res=res
        self.db=db

    def Create(self,values={}):
        newObj=self.model(**values)
        db.session.add(newObj)
        db.session.commit()
        return newObj
    
    def Update(self,key,values={}):
        query = self.Query(filters=key)
        obj = query.first()
        if obj:
            query.update(values)
        db.session.commit()
        return obj
    
    def UpdateMany(self,key,values={}):
        query = self.Query(filters=key)        
        query.update(values)
        db.session.commit()
        return query.all()
    
    def Filter(self,query,filters):
        return query.filter(*filters)
    
    def Query(self,filters=[],joins=[]):
        query = self.model.query
        if len(joins)>0:
            for join in joins:
                query = query.join(join['table'],join['key'])
        if len(filters)>0:
            query = self.Filter(query,filters)
        return query

    def GetAll(self,filters=[],query=None):
        if not query:
            query = self.Query(filters=filters)
        return query.all()
    
    def GetFirst(self,filters=[],query=None):
        if not query:
            return self.Query(filters=filters).first()
        return self.Filter(query,filter).first()
    
    def Delete(self,filters=[],commit=True):
        query = self,query(filters=filters)
        query.delete()
        if commit:
            db.session.commit()
        return True
    
    def AddColumns(self,query,columns=[]):
        val = query.add_columns(*columns)
        return val
    
    def WithColumns(self,query,columns=[],distinct=False):
        val = query.with_entities(*columns)
        if distinct:
            val = val.distinct()
        return val
    
    def CreateIfNotExists(self,filters=[],values={}):
        check = self.GetFirst(filter)
        if check:
            return False
        return self.Create(values)
    
    def OrderBy(self,query,keys):
        return query.order_by(*keys)
    