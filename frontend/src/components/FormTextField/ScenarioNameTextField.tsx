import React from 'react';
import CastleIcon from '@mui/icons-material/Castle';
import NameTextField from './NameTextField';

interface ScenarioNameTextFieldProps {
  value: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  editable?: boolean;
}

const ScenarioNameTextField: React.FC<ScenarioNameTextFieldProps> = ({ value, onChange, placeholder = '', editable = true }) => {
  return (
    <NameTextField
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      editable={editable}
      icon={<CastleIcon />}
    />
  );
}

export default ScenarioNameTextField;
