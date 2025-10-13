import pyodbc

class YOLOResultsDB:
    def __init__(self, server, database, user, password):
        self.conn_str = (
            f"DRIVER={{SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password}"
        )
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()

    def save_results(self, identificador_web, results):
        """
        Guarda los resultados de YOLO en la base de datos.
        """
        for box in results.boxes:
            clase = results.names[int(box.cls)]
            conf = float(box.conf)
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            query = """
                INSERT INTO [dbo].[DeteccionesYolo]  ([web],[clase],[confianza],[x1],[y1],[x2],[y2])
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, identificador_web, clase, conf, x1, y1, x2, y2)

        self.conn.commit()

    def get_results_por_web(self, identificador_web):
        """
        Devuelve todos los registros filtrando por el campo 'web'.
        """
        query = "SELECT * FROM [dbo].[DeteccionesYolo] WHERE [web] = ?"
        self.cursor.execute(query, identificador_web)
        rows = self.cursor.fetchall()
        # Opcional: convertir a lista de diccionarios
        results = []
        columns = [column[0] for column in self.cursor.description]
        for row in rows:
            results.append(dict(zip(columns, row)))
        return results

    def close(self):
        self.cursor.close()
        self.conn.close()