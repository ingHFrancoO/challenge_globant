from pipeline.pipeline import pipeline
from persistence.restore import restore_table_from_gcs_backup

_RESTORE_INFO={
    'table_name': 'departments',
    'backup_date': '20251230_06024211'
}

def main(restore=False):
    if restore:
        restore_table_from_gcs_backup(_RESTORE_INFO['table_name'], _RESTORE_INFO['backup_date'] )
        return 
    
    pipeline()

if __name__ == '__main__':
    main(True)