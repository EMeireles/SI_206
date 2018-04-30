import sqlite3
import csv
import json

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'


def init_db(db_name,csv_file):
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)

    cur_Start=conn.cursor()

    statement='DROP TABLE IF EXISTS "Countries"'

    cur_Start.execute(statement)
    conn.commit()

    statement='DROP TABLE IF EXISTS "Bars"'
    cur_Start.execute(statement)
    conn.commit()

    cur_Countries=conn.cursor()

    statement='''
    CREATE TABLE "Countries"(
    "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Alpha2" TEXT NOT NULL,
    "Alpha3" TEXT NOT NULL,
    "EnglishName" TEXT NOT NULL,
    "Region" TEXT NOT NULL,
    "Subregion" TEXT NOT NULL,
    "Population" INTEGER NOT NULL,
    "Area" REAL
    )
    '''

    cur_Countries.execute(statement)
    conn.commit()

    cur_Bars=conn.cursor()

    statement='''
    CREATE TABLE "Bars"(
    "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Company" TEXT NOT NULL,
    "SpecificBeanBarName" TEXT NOT NULL,
    "REF" TEXT NOT NULL,
    "ReviewDate" TEXT NOT NULL,
    "CocoaPercent" REAL NOT NULL,
    "CompanyLocation" TEXT NOT NULL,
    "CompanyLocationId" INTEGER,
    "Rating" REAL NOT NULL,
    "BeanType" TEXT NOT NULL,
    "BroadBeanOrigin" TEXT NOT NULL,
    "BroadBeanOriginId" INTEGER,
    FOREIGN KEY (BroadBeanOriginId) REFERENCES Countries(Id),
    FOREIGN KEY (CompanyLocationId) REFERENCES Countries(Id)
    )
    '''

    cur_Bars.execute(statement)
    conn.commit()

    csv_list=[]
    coutntry_tups=[]

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for item in reader:
            csv_list.append((item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]))

    with open(COUNTRIESJSON, 'r') as f:
        datastore = json.load(f)
        for dic in datastore:
            coutntry_tups.append((dic['alpha2Code'],dic['alpha3Code'],dic['name'],dic['region'],dic['subregion'],dic['population'],dic['area']))
    

    cur_Insert=conn.cursor()
    for countries in coutntry_tups:
        insertion = (None, countries[0], countries[1], countries[2], countries[3],countries[4],countries[5],countries[6])
        statement = 'INSERT INTO "Countries" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur_Insert.execute(statement, insertion)

    conn.commit()

    cur_Insert2=conn.cursor()
    for bars in csv_list[1:]:
        if bars[7]=='':
            bar="No Information"
        else:
            bar=bars[7]
        insertion = (None, bars[0], bars[1], bars[2], bars[3],bars[4][:-1],bars[5],0,bars[6],bar,bars[8],0)
        statement = 'INSERT INTO "Bars" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur_Insert2.execute(statement, insertion)

        update='''
        UPDATE Bars SET CompanyLocationId=(SELECT Id FROM Countries WHERE Bars.CompanyLocation=Countries.EnglishName)
        '''
        cur_FID=conn.cursor()
        cur_FID.execute(update)

        update='''
        UPDATE Bars SET BroadBeanOriginId=(SELECT Id FROM Countries WHERE Bars.BroadBeanOrigin=Countries.EnglishName)
        '''
        cur_FID=conn.cursor()
        cur_FID.execute(update)


    conn.commit()
    conn.close()

# Part 2: Implement logic to process user commands
def process_command(command):
    logic=command.split()
    conn=sqlite3.connect(DBNAME)
    


    if logic[0]=='bars':
        params_dic={'sellcountry':None,
            'sourcecountry':None,
            'sellregion':None,
            'sourceregion':None,
            'sort':'ratings',
            'order':' DESC',
            'lim':10}
        
        for item in logic:
            sort_list=item.split("=")
            if sort_list[0]=='ratings':
                params_dic['sort']='ratings'
            elif sort_list[0]=='cocoa':
                params_dic['sort']='cocoa'
            elif sort_list[0]=='sellcountry':
                params_dic['sellcountry']=sort_list[1]
            elif sort_list[0]=='sourcecountry':
                params_dic['sourcecountry']=sort_list[1]
            elif sort_list[0]=='sellregion':
                params_dic['sellregion']=sort_list[1]
            elif sort_list[0]=='sourceregion':
                params_dic['sourceregion']=sort_list[1]
            elif sort_list[0]=='top':
                params_dic['order']=' DESC'
                params_dic['lim']=sort_list[1]
            elif sort_list[0]=='bottom':
                params_dic['order']=' ASC'
                params_dic['lim']=sort_list[1]
            elif sort_list[0]!='bars':
                return False
        
        
        if params_dic['sellregion'] != None:
            cur=conn.cursor()
            
            if params_dic['sort']=='cocoa':
                s="B.CocoaPercent"
            else:
                s="B.Rating"

            statement='''
            SELECT B.SpecificBeanBarName,B.Company,B.CompanyLocation,B.Rating,B.CocoaPercent,B.BroadBeanOrigin
            FROM Bars AS B
            JOIN Countries as C
            ON B.CompanyLocationId=C.Id
            WHERE C.Region= '''+"'{}'".format(params_dic['sellregion'])+'''
            ORDER BY '''+s+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])
            cur.execute(statement)
            results=cur.fetchall()
            return results

        elif params_dic['sellcountry'] != None:
            cur=conn.cursor()
            
            if params_dic['sort']=='cocoa':
                s="B.CocoaPercent"
            else:
                s="B.Rating"
            statement='''
            SELECT B.SpecificBeanBarName,B.Company,B.CompanyLocation,B.Rating,B.CocoaPercent,B.BroadBeanOrigin
            FROM Bars AS B
            JOIN Countries as C
            ON B.CompanyLocationId=C.Id
            WHERE C.Alpha2= '''+"'{}'".format(params_dic['sellcountry'])+'''
            ORDER BY '''+s+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])
            cur.execute(statement)
            results=cur.fetchall()
            return results

        elif params_dic['sourcecountry'] != None:
            cur=conn.cursor()
            
            if params_dic['sort']=='cocoa':
                s="B.CocoaPercent"
            else:
                s="B.Rating"
            statement='''
            SELECT B.SpecificBeanBarName,B.Company,B.CompanyLocation,B.Rating,B.CocoaPercent,B.BroadBeanOrigin
            FROM Bars AS B
            JOIN Countries as C
            ON B.BroadBeanOriginId=C.Id
            WHERE C.Alpha2= '''+"'{}'".format(params_dic['sourcecountry'])+'''
            ORDER BY '''+s+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])
            cur.execute(statement)
            
            results=cur.fetchall()
            return results
            
        elif params_dic['sourceregion'] != None:
            cur=conn.cursor()
            
            if params_dic['sort']=='cocoa':
                s="B.CocoaPercent"
            else:
                s="B.Rating"
            statement='''
            SELECT B.SpecificBeanBarName,B.Company,B.CompanyLocation,B.Rating,B.CocoaPercent,B.BroadBeanOrigin
            FROM Bars AS B
            JOIN Countries as C
            ON B.BroadBeanOriginId=C.Id
            WHERE C.Region= '''+"'{}'".format(params_dic['sourceregion'])+'''
            ORDER BY '''+s+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])
            cur.execute(statement)
            results=cur.fetchall()
            return results
        else:
            cur=conn.cursor()
            
            if params_dic['sort']=='cocoa':
                s="B.CocoaPercent"
            else:
                s="B.Rating"

            statement='''
            SELECT B.SpecificBeanBarName,B.Company,B.CompanyLocation,B.Rating,B.CocoaPercent,B.BroadBeanOrigin
            FROM Bars AS B
            ORDER BY ''' + s+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])
            cur.execute(statement)
            
            results=cur.fetchall()
            return results

    elif logic[0]=='companies':
        params_dic={'country':None,
        'region':None,
        'sort':'ratings',
        'order':'DESC',
        'lim':10}

        for item in logic:
            sort_list=item.split("=")
            if sort_list[0]=='ratings':
                params_dic['sort']='ratings'
            elif sort_list[0]=='cocoa':
                params_dic['sort']='cocoa'
            elif sort_list[0]=='bars_sold':
                params_dic['sort']='bars_sold'
            elif sort_list[0]=='country':
                params_dic['country']=sort_list[1]
            elif sort_list[0]=='region':
                params_dic['region']=sort_list[1]
            elif sort_list[0]=='top':
                params_dic['order']=' DESC'
                params_dic['lim']=sort_list[1]
            elif sort_list[0]=='bottom':
                params_dic['order']=' ASC'
                params_dic['lim']=sort_list[1]
            elif sort_list[0]!='companies':
                return False

        if params_dic['country'] !=None:
            cur=conn.cursor()
    
            if params_dic['sort']=='ratings':
                s="AVG(B.Rating)"
            elif params_dic['sort']=='cocoa':
                s="AVG(B.CocoaPercent)"
            elif params_dic['sort']=='bars_sold':
                s="COUNT(B.SpecificBeanBarName)"
            statement='''
            SELECT B.Company, B.CompanyLocation,'''+s+'''
            FROM Bars AS B
            JOIN Countries AS C
            ON B.CompanyLocationId=C.Id
            WHERE C.Alpha2= ''' + "'{}'".format(params_dic['country'])+'''
            GROUP BY B.Company
            HAVING COUNT(B.SpecificBeanBarName) > 4
            ORDER BY '''+s+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])
            cur.execute(statement)
            results=cur.fetchall()
            return results


        elif params_dic['region'] != None:
            cur=conn.cursor()
            
            if params_dic['sort']=='ratings':
                s="AVG(B.Rating)"
            elif params_dic['sort']=='cocoa':
                s="AVG(B.CocoaPercent)"
            elif params_dic['sort']=='bars_sold':
                s="COUNT(B.SpecificBeanBarName)"

            statement='''
            SELECT B.Company, B.CompanyLocation, '''+s+'''
            FROM Bars AS B
            JOIN Countries AS C
            ON B.CompanyLocationId=C.Id
            WHERE C.Region= '''+ "'{}'".format(params_dic['region'])+'''
            GROUP BY B.Company
            HAVING COUNT(B.SpecificBeanBarName) > 4
            ORDER BY '''+s+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])

            cur.execute(statement)
            results=cur.fetchall()
            return results
        else:
            cur=conn.cursor()
            
            if params_dic['sort']=='ratings':
                s="AVG(B.Rating)"
            elif params_dic['sort']=='cocoa':
                s="AVG(B.CocoaPercent)"
            elif params_dic['sort']=='bars_sold':
                s="COUNT(B.SpecificBeanBarName)"

            statement='''
            SELECT B.Company, B.CompanyLocation, '''+s+'''
            FROM Bars AS B
            GROUP BY B.Company
            HAVING COUNT(B.SpecificBeanBarName) > 4
            ORDER BY '''+ s+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])
            cur.execute(statement)

            results=cur.fetchall()
            return results

    elif logic[0]=='countries':

        params_dic={'region':None,
        'sort_1':'sellers',
        'sort_2':'ratings',
        'sort':'ratings',
        'order':'DESC',
        'lim':10}

        for item in logic:
            sort_list=item.split("=")
            if sort_list[0]=='ratings':
                params_dic['sort_2']='ratings'
            elif sort_list[0]=='cocoa':
                params_dic['sort_2']='cocoa'
            elif sort_list[0]=='bars_sold':
                params_dic['sort_2']='bars_sold'
            elif sort_list[0]=='sellers':
                params_dic['sort_1']='sellers'
            elif sort_list[0]=='sources':
                params_dic['sort_1']='sources'
            elif sort_list[0]=='region':
                params_dic['region']=sort_list[1]
            elif sort_list[0]=='top':
                params_dic['order']=' DESC'
                params_dic['lim']=sort_list[1]
            elif sort_list[0]=='bottom':
                params_dic['order']=' ASC'
                params_dic['lim']=sort_list[1]
            elif sort_list[0]!='countries':
                return False
            

        if params_dic['region']!=None:

            cur=conn.cursor()
            
            if params_dic['sort_1']=='sellers':
                s_1="B.CompanyLocationId"
            elif params_dic['sort_1']=='sources':
                s_1="B.BroadBeanOriginId"

            if params_dic['sort_2']=='ratings':
                s_2="AVG(B.Rating)"
            elif params_dic['sort_2']=='cocoa':
                s_2="AVG(B.CocoaPercent)"
            elif params_dic['sort_2']=='bars_sold':
                s_2="COUNT(B.SpecificBeanBarName)"

            statement='''
            SELECT C.EnglishName,C.Region,'''+s_2+'''
            FROM Countries AS C
            JOIN Bars AS B 
            ON C.Id= '''+s_1+'''
            WHERE C.Region= ''' + "'{}'".format(params_dic['region']) + '''
            GROUP BY C.EnglishName
            HAVING COUNT(B.SpecificBeanBarName)>4
            ORDER BY '''+s_2+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])
            
            cur.execute(statement)
            results=cur.fetchall()
            return results
        else:
            cur=conn.cursor()
            
            if params_dic['sort_1']=='sellers':
                s_1="B.CompanyLocationId"
            elif params_dic['sort_1']=='sources':
                s_1="B.BroadBeanOriginId"

            if params_dic['sort_2']=='ratings':
                s_2="AVG(B.Rating)"
            elif params_dic['sort_2']=='cocoa':
                s_2="AVG(B.CocoaPercent)"
            elif params_dic['sort_2']=='bars_sold':
                s_2="COUNT(B.SpecificBeanBarName)"

            statement='''
            SELECT C.EnglishName,C.Region,'''+s_2+'''
            FROM Countries AS C
            JOIN Bars AS B 
            ON C.Id= ''' +s_1+'''
            GROUP BY C.EnglishName
            HAVING COUNT(B.SpecificBeanBarName)>4
            ORDER BY '''+s_2+ params_dic['order']+'''
            LIMIT '''+str(params_dic['lim'])

            cur.execute(statement)
            results=cur.fetchall()
            return results

    elif logic[0]=='regions':

        params_dic={
        'sort_1':'sellers',
        'sort_2':'ratings',
        'sort':'ratings',
        'order':'DESC',
        'lim':10}

        for item in logic:
            sort_list=item.split("=")
            if sort_list[0]=='ratings':
                params_dic['sort_2']='ratings'
            elif sort_list[0]=='cocoa':
                params_dic['sort_2']='cocoa'
            elif sort_list[0]=='bars_sold':
                params_dic['sort_2']='bars_sold'
            elif sort_list[0]=='sellers':
                params_dic['sort_1']='sellers'
            elif sort_list[0]=='sources':
                params_dic['sort_1']='sources'
            elif sort_list[0]=='top':
                params_dic['order']=' DESC'
                params_dic['lim']=sort_list[1]
            elif sort_list[0]=='bottom':
                params_dic['order']=' ASC'
                params_dic['lim']=sort_list[1]
            elif sort_list[0]!='regions':
                return False

        cur=conn.cursor()
            
        if params_dic['sort_1']=='sellers':
            s_1="B.CompanyLocationId"
        elif params_dic['sort_1']=='sources':
            s_1="B.BroadBeanOriginId"

        if params_dic['sort_2']=='ratings':
            s_2="AVG(B.Rating)"
        elif params_dic['sort_2']=='cocoa':
            s_2="AVG(B.CocoaPercent)"
        elif params_dic['sort_2']=='bars_sold':
            s_2="COUNT(B.SpecificBeanBarName)"

        statement='''
        SELECT C.Region,'''+s_2+'''
        FROM Countries AS C
        JOIN BARS AS B
        ON C.Id= ''' + s_1+'''
        GROUP BY C.Region
        HAVING COUNT(B.SpecificBeanBarName) > 4
        ORDER BY '''+s_2+ params_dic['order']+'''
        LIMIT '''+str(params_dic['lim'])
        
        cur.execute(statement)
        results=cur.fetchall()
        return results
    
    else:
        return False
        
        



def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command:')

        if response == 'help':
            print(help_text)
            continue
        else:
            try:
                db=process_command(response)
                logic=response.split()
                if logic[0]=='bars' and db!=False:
                    if len(db)>0:
                        for item in db:
                            if len(item[0])>13:
                                new_0=item[0][:12]+"..."
                            else:
                                new_0=item[0]
                            if len(item[1])>13:
                                new_1=item[1][:12]+"..."
                            else:
                                new_1=item[1]
                            if len(item[2])>13:
                                new_2=item[2][:12]+"..."
                            else:
                                new_2=item[2]
                            if len(item[5])>13:
                                new_5=item[5][:12]+"..."
                            else:
                                new_5=item[5]
                            print('{:<20}'.format(new_0),'{:<20}'.format(new_1),'{:<20}'.format(new_2),'{:<20}'.format(item[3]),'{:<20}'.format(str(item[4])+'%'),'{:<20}'.format(new_5))
                    else:   
                        print("Sorry No Results!")

                elif logic[0]=='regions'and db!=False :
                    if len(db)>0:
                        for item in db:
                            print('{:<20}'.format(item[0]),'{:<15}'.format(item[1]))
                    else:
                        print("Sorry no Results!")

                elif (logic[0]=='countries' or logic[0]=='companies') and db!=False :
                    if len(db)>0:
                        for item in db[:10]:
                            if len(item[0])>13:
                                new_0=item[0][:12]+"..."
                            else:
                                new_0=item[0]
                            if len(item[1])>13:
                                new_1=item[1][:12]+"..."
                            else:
                                new_1=item[1]
                            print('{:<20}'.format(new_0),'{:<20}'.format(new_1),'{:<20}'.format(item[2]))
                    else:
                        print("Sorry no Results!")
                else:
                    print("Command Not Recognized:{}".format(response))
                    
            except:
                print("Command Not Recognized:{}".format(response))




# Uncomment the Init DB function to initialize database on first run, comment it out after first use to use search functions 
if __name__=="__main__":
    #init_db(DBNAME,BARSCSV)
    interactive_prompt()