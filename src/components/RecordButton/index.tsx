import { memo } from 'react';
import { Button } from '@mui/material';
import { usePythonApi } from '../../hooks/pythonBridge'

import styles from './index.module.css';

function RecordButton() {
    const startRecord = () => {
        usePythonApi('record', '')
    };
  
    const stopRecord = () => {
        usePythonApi('stop_record', '')
    };
  
    return (
        <div className={styles.centerBtn}>
            <Button
                onMouseDown={startRecord}
                onMouseUp={stopRecord}
                onMouseLeave={stopRecord}
            >
                <span>Record</span>
            </Button>
        </div>
    );
}

export default memo(RecordButton);
