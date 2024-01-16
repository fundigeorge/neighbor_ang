use sites
go

SELECT * from sys.tables
go
-- Create a new table called 'transmitter_cellname' in schema 'dbo'
-- Drop the table if it already exists
IF OBJECT_ID('dbo.transmitter_cellname', 'U') IS NOT NULL
DROP TABLE dbo.transmitter_cellname
GO

--Copy the transmitter table to transmitter cellname table
-- the into copy and create a new table
SELECT site, transmitter 
into transmitter_cellname
from umts_transmitter
go

select COUNT(*)  from transmitter_cellname
-- Add a new column 'cell_name' to table 'TableName' in schema 'SchemaName'
-- Drop 'cell_name' from table 'transmitter_cellname' in schema 'dbo' if it exist
-- Drop the table 'TableName' in schema 'SchemaName'
IF COL_LENGTH('transmitter_cellname', 'cell_name') IS NOT NULL 
    ALTER TABLE dbo.transmitter_cellname
    DROP COLUMN cell_name
    GO

-- Add a new column 'cell_name' to table 'TableName' in schema 'SchemaName'
ALTER TABLE dbo.transmitter_cellname
    ADD cell_name /*new_column_name*/ NVARCHAR(50) /*new_column_datatype*/ NULL /*new_column_nullability*/
GO


--generate dummy cellname
--Update rows in table 'transmitter_cellname'transmitter_cellname
-- Update rows in table 'transmitter_cellname'
UPDATE transmitter_cellname
SET
    cell_name = site + '-' + RIGHT(transmitter,1);
    -- add more columns and values here
GO

SELECT top 5 *  from transmitter_cellname
GO
