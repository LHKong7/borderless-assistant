import { memo, useState } from 'react';
import { Button, Tooltip } from '@mui/material';
import { usePythonApi } from '../../hooks/pythonBridge'

import Wave from 'react-wavify'

import styles from './index.module.css';

function RecordButton() {
    const [isRecording, setIsRecording] = useState(false);

    const startRecord = () => {
        usePythonApi('record', '');
        setIsRecording(true);
    };
  
    const stopRecord = () => {
        usePythonApi('stop_record', '');
        setIsRecording(false);
    };
  
    return (
        <div className={styles.centerBtn}>
            {/* 悬浮提示：引导用户按住录音 */}
            <Tooltip title="按住按钮开始录音，松开结束录音" arrow>
                <Button
                    className={styles.recordBtn}
                    onMouseDown={startRecord}
                    onMouseUp={stopRecord}
                    onMouseLeave={stopRecord}
                >
                    <span>🎙 录音</span>
                </Button>
            </Tooltip>

            {/* 录音波形动画（仅在录音时显示） */}
            {isRecording && (
                <Wave
                    fill="#1277b0"
                    paused={false}
                    options={{
                        height: 30,
                        amplitude: 30,
                        speed: 0.25,
                        points: 4,
                    }}
                    className={styles.wave}
                />
            )}
        </div>
    );
}

export default memo(RecordButton);
