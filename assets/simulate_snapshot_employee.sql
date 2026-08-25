-- Change the dbt_valid_from before July
--
-- UPDATE snapshots.employees_snapshot
-- SET dbt_valid_from = '2026-01-01 00:00:00';

-- Change the 'Alice' role
--
-- UPDATE raw.employees SET role = 'branch_admin' WHERE id=1;

-- Update the 'Alice' role change on the snaphots to the 2026-07-15
--
-- UPDATE snapshots.employees_snapshot 
-- SET dbt_valid_to = '2026-07-15 00:00:00'
-- WHERE dbt_valid_to IS NOT NULL
--
-- UPDATE snapshots.employees_snapshot
-- SET dbt_valid_from = '2026-07-15 00:00:00'
-- WHERE dbt_valid_to IS NULL
-- AND id IN (SELECT id FROM snapshots.employees_snapshot WHERE dbt_valid_to IS NOT NULL)

-- select * from snapshots.employees_snapshot

-- select * from raw.employees;