import aiohttp_jinja2
import docker

#global variable for no. of times of load.
refresh = 0

@aiohttp_jinja2.template("layout.html")
async def monitor(request):
    #data loaded for the first time from the function call
    global refresh
    db = request.app['db']
    await db.collection.drop()
    
    if refresh == 0:
        
        try:
            #Client creation
            client = docker.from_env()
            container_list = client.containers.list(all=True)
            
        except:
            return {"result": "client creation failure"}    
        try:    
            result_list = []
            for i in container_list:
                st = str(i)[12:-1]
                dic1 = {}
                container = client.containers.get(st)
                dic1['container_name'] = container.attrs['Name']
                dic1['started_at'] = container.attrs['State']['StartedAt']
                dic1['status'] = container.attrs['State']['Status']
                try:
                    dic1['ram'] = container.stats(stream=False)['memory_stats']['usage']
                except:
                    dic1['ram'] = 0
                dic1['cpu'] = container.stats(stream=False)['cpu_stats']['cpu_usage']['total_usage']
                result_list.append(dic1)
        except:
            return {"result": "data not found"}
        
        try:
            await db.collection.insert_many(i for i in result_list)

        except:
            return {"result": "data not stored in the db"}
        refresh+=1
        return {'container_list': result_list}
    
    #data retrieved from the database after refresh 
    else:
        result_list = []
        async for document in db.collection.find():
            result_list.append(document)   
        return {"result_list" : result_list} 
