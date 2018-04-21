from BuildDatabase import *
import DrawAirbase as DA
import unittest


class TestClass(unittest.TestCase):
    def class_test(self):
        test_basename = "testbase"
        test_lat = 30
        test_lon = 120
        A = DA.AirBase(test_basename, test_lat, test_lon)
        self.assertEqual(A.basename, test_basename)
        self.assertEqual(A.lat, test_lat)
        self.assertEqual(A.lon, test_lon)

class TestCaching(unittest.TestCase):
    def squad_json_test(self):
        ts = Squad_CD[0]
        self.assertEqual(ts["squad_nm"], "18th Aggressor Squadron")
        self.assertEqual(ts["command_nm"], "Pacific Air Forces")
        self.assertEqual(ts["wing_nm"], "354th FW")
        self.assertEqual(ts["base_nm"], "Eielson AFB")
        self.assertEqual(ts["aircraft_nm"], "F-16C/D")
        self.assertEqual(ts["base_url"], "/wiki/Eielson_Air_Force_Base")
        self.assertEqual(ts["aircraft_url"], "/wiki/F-16_Fighting_Falcon")
        self.assertEqual(ts["BAid"], "F16")

    def base_json_test(self):
        ts = Base_CD[0]
        self.assertEqual(ts["base_nm"], "Eielson AFB")
        self.assertEqual(ts["url"], "/wiki/Eielson_Air_Force_Base")
        self.assertEqual(ts["lat"], 64.665556)
        self.assertEqual(ts["lon"], -147.101389)

class TestDataBase(unittest.TestCase):
    def test_squad_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()


        sql = 'SELECT SquadName FROM Squad'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('27th Fighter Squadron',), result_list)
        self.assertEqual(len(result_list), 163)

        sql = '''
                    SELECT SquadName, Id FROM Squad
                    WHERE BattleAircraftCode LIKE "F15"
                    ORDER BY Id
                '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 21)
        self.assertEqual(result_list[0][1], 66)

        sql = '''
                SELECT BaseName FROM AirBase
                '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 75)
        self.assertIn(('Aviano AB',), result_list)

        sql = '''
                SELECT AircraftName FROM Aircraft
                '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 6)
        self.assertIn(('F22',), result_list)

        sql = '''
                SELECT A.MaxSpeed, A.CombatRadius, B.Latitude, B.Longitude, A.AircraftName, B.BaseName, S.SquadName
                FROM Squad AS S
                JOIN Aircraft  AS A 
                    ON S.BattleAircraftCode = A.AircraftName
                JOIN Airbase AS B 
                    ON B.BaseName = S.BaseNAme
                WHERE B.Id = 18
                ORDER BY S.Id
                '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 5)
        self.assertEqual(result_list[0][6], "41st Airlift Squadron")
        self.assertEqual(result_list[0][5], "Little Rock Air Force Base")
        self.assertEqual(result_list[0][3], -92.146389)
        self.assertEqual(result_list[0][2], 34.916944)
        self.assertEqual(result_list[0][1], 0.0)
        self.assertEqual(result_list[0][0], 0.0)

        conn.close()



class TestDataBase2(unittest.TestCase):
    def test_base_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
                        SELECT BaseName FROM AirBase
                        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 75)
        self.assertIn(('Aviano AB',), result_list)


        conn.close()


class TestDataBase3(unittest.TestCase):
    def test_join_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
                        SELECT A.MaxSpeed, A.CombatRadius, B.Latitude, B.Longitude, A.AircraftName, B.BaseName, S.SquadName
                        FROM Squad AS S
                        JOIN Aircraft  AS A 
                            ON S.BattleAircraftCode = A.AircraftName
                        JOIN Airbase AS B 
                            ON B.BaseName = S.BaseNAme
                        WHERE B.Id = 18
                        ORDER BY S.Id
                        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 5)
        self.assertEqual(result_list[0][6], "41st Airlift Squadron")
        self.assertEqual(result_list[0][5], "Little Rock Air Force Base")
        self.assertEqual(result_list[0][3], -92.146389)
        self.assertEqual(result_list[0][2], 34.916944)
        self.assertEqual(result_list[0][1], 0.0)
        self.assertEqual(result_list[0][0], 0.0)

        conn.close()


        conn.close()



if __name__ == '__main__':
    unittest.main()