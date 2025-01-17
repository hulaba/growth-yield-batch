#!/usr/bin/env python
"""
Take directory of csvs created by the growth-yield-batch process
and import them to a sqlite3 TABLE
"""
import sqlite3
import glob
import csv
import os


CSVDIR = os.curdir
FILTER = "var*.csv"
DATABASE = "data.db"


def data_generator():
    csv_paths = glob.glob(os.path.join(CSVDIR, 'final', FILTER))
    for csv_path in csv_paths:
        fvsreader = csv.reader(open(csv_path, 'rb'), delimiter=',', quotechar='"')
        fvsreader.next()  # skip header
        for row in fvsreader:
            # only yield a row if it has data in first column (AGL)
            if row[0]:
                yield row


if __name__ == "__main__":
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    try:
        cur.execute("""
    CREATE TABLE trees_fvsaggregate (
        agl double precision,
        bgl double precision,
        calc_carbon double precision,
        climate character varying(20),
        cond integer NOT NULL,
        dead double precision,
        "offset" integer NOT NULL,
        rx integer NOT NULL,
        site integer NOT NULL,
        total_stand_carbon double precision,
        var character varying(2) NOT NULL,
        year double precision NOT NULL,
        merch_carbon_removed double precision,
        merch_carbon_stored double precision,
        cedr_bf double precision,
        cedr_hrv double precision,
        ch_cf double precision,
        ch_hw double precision,
        ch_tpa double precision,
        cut_type double precision,
        df_bf double precision,
        df_hrv double precision,
        es_btl double precision,
        firehzd double precision,
        hw_bf double precision,
        hw_hrv double precision,
        lg_cf double precision,
        lg_hw double precision,
        lg_tpa double precision,
        lp_btl double precision,
        mnconbf double precision,
        mnconhrv double precision,
        mnhw_bf double precision,
        mnhw_hrv double precision,
        nsodis double precision,
        nsofrg double precision,
        nsonest double precision,
        pine_bf double precision,
        pine_hrv double precision,
        pp_btl double precision,
        sm_cf double precision,
        sm_hw double precision,
        sm_tpa double precision,
        spprich double precision,
        sppsimp double precision,
        sprc_bf double precision,
        sprc_hrv double precision,
        wj_bf double precision,
        wj_hrv double precision,
        ww_bf double precision,
        ww_hrv double precision,
        after_ba integer,
        after_merch_bdft integer,
        after_merch_ft3 integer,
        after_total_ft3 integer,
        after_tpa integer,
        age integer,
        removed_merch_bdft integer,
        removed_merch_ft3 integer,
        removed_total_ft3 integer,
        removed_tpa integer,
        start_ba integer,
        start_merch_bdft integer,
        start_merch_ft3 integer,
        start_total_ft3 integer,
        start_tpa integer
    );
        """)
        print "Created fvsaggregate table"
    except:
        print "Table already exists"

    print "Inserting data into table"
    sql = "INSERT INTO trees_fvsaggregate VALUES (%s);" % (",".join("?"*66))
    cur.executemany(sql, data_generator())

    con.commit()
    cur.close()

    print """ Now manually create indexes:
        CREATE INDEX idx_trees_fvsaggregate_var ON trees_fvsaggregate (var);
        CREATE INDEX idx_trees_fvsaggregate_year ON trees_fvsaggregate (year);
        CREATE INDEX idx_trees_fvsaggregate_cond ON trees_fvsaggregate (cond);
        CREATE INDEX idx_trees_fvsaggregate_rx ON trees_fvsaggregate (rx);
        CREATE INDEX idx_trees_fvsaggregate_offset ON trees_fvsaggregate ("offset");
    """
