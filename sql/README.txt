This directory holds some tools for configuring the LOST database and migrating legacy OSNAP data. This project is complex enough that no two people are likely to write the same logic with the same structure. Direct use of this code in your own project will result in 0 points awarded for the data migration portion of the final project.

Files:
README.txt - This readme file
create_tables.sql   - A script to generate the base tables
import_data.sh      - A script to import OSNAP legacy data
do_transit.py       - Processes the transit data
facilities_map.sql  - Loads the static data on the facilities
norm_tags.py        - Rewrites some of the data so that it is easier to process
prep_inv.py         - Converts *_inventory.csv to sql
prep_prod.py        - Converts product info to sql
prep_sec.py         - Converts security info to sql
prepend_fcode       - Concatenates the inventory data and annotates with source facility
waypoints.py        - Processes the convoy file
backfill.sql        - A script to fill in a few inferrences



-------------------------------------
-- First cut at queries for testing with OSNAP data imported
-------------------------------------
To test the LOST database after the OSNAP data has been migrated, the following queries have been suggests. These queries are untested but should have the right basic structure. If you compare the queries to the entity relationship diagram you should be able to trace the path between the assets and facilities.

/* This query successfully returning all assets at least once is enough to get credit */
SELECT fcode,asset_tag
FROM assets a
LEFT JOIN asset_at aa  ON a.asset_pk=aa.asset_fk
LEFT JOIN facilities f ON aa.facility_fk=f.facility_pk

/* This query is more complex... only the facility an asset is currently at. Assets in transit will be missed */
SELECT fcode,asset_tag 
FROM assets a
JOIN asset_at aa  ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
WHERE aa.arrive_dt < now() and (aa.depart_dt is NULL or aa.depart_dt > now())

/* This query should pick up the assets currently in transit */
SELECT request_id,asset_tag 
FROM assets a
JOIN asset_on aa  ON a.asset_pk=aa.asset_fk
JOIN convoys c ON aa.convoy_fk=c.convoy_pk
WHERE aa.load_dt < now() and (aa.unload_dt is NULL or aa.unload_dt > now())
