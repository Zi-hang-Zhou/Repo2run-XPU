import os
import psycopg2
import json

# 连接数据库
DB_URL = os.environ.get("DATABASE_URL", "postgresql://zihang:zihang123@localhost:5432/xpu_db")

def check_scores():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # 查询 hits 大于 0 的条目，按 hits 降序排列
        # 注意：这里我们要看 telemetry 里的原始 json 数据
        cur.execute("""
            SELECT id, telemetry 
            FROM xpu_entries 
            WHERE (telemetry->>'hits')::numeric > 0 
            ORDER BY (telemetry->>'hits')::numeric DESC
            LIMIT 10;
        """)
        
        rows = cur.fetchall()
        
        print(f"\n{'ID':<40} | {'Hits (分数)'}")
        print("-" * 60)
        
        for row in rows:
            xpu_id, telemetry = row
            hits = telemetry.get('hits', 0)
            
            # 重点：检查是不是浮点数
            is_float = isinstance(hits, float) or (isinstance(hits, str) and '.' in hits)
            
            print(f"{xpu_id:<40} | {hits} {'✨(小数!)' if is_float else ''}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    check_scores()