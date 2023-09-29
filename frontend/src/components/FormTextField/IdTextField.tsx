import React from 'react';
import NumbersIcon from '@mui/icons-material/Numbers';
import FormTextField from './FormTextField';

interface IdTextFieldProps {
  value: number;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: number;
  editable?: boolean;
}
const IdTextField: React.FC<IdTextFieldProps> = ({ value, onChange, placeholder = '', editable = true }) => {

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const idPattern = /^[0-9]{0,3}$/;
    const value = e.target.value
    if (idPattern.test(value)) {
      if (onChange !== undefined) { onChange(e); }
    }
  };

  return (
    <FormTextField
      id="id"
      name="_id"
      label="ID"
      value={value.toString()}
      onChange={handleChange}
      placeholder={placeholder.toString()}
      editable={editable}
      icon={<NumbersIcon />}
    />
  );
}

export default IdTextField;
