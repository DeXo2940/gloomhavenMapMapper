import React from 'react';
import MapIcon from '@mui/icons-material/Map';
import FormTextField from './FormTextField';

interface CoordinatesTextFieldProps {
  value: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  editable?: boolean;
}

const CoordinatesTextField: React.FC<CoordinatesTextFieldProps> = ({ value, onChange, placeholder = '', editable = true }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const coordinatePattern = /^(([A-z])|([A-z]-)|([A-z]-\d{1,2}))$/;
    e.target.value = e.target.value.toUpperCase()
    const value = e.target.value
    if (value === '' || coordinatePattern.test(value)) {
      if (onChange !== undefined) { onChange(e); }
    }
  };

  return (
    <FormTextField
      id='coordinates'
      name='coordinates'
      label='Coordinates'
      value={value}
      onChange={handleChange}
      placeholder={placeholder}
      editable={editable}
      icon={<MapIcon />}
    />
  );
}

export default CoordinatesTextField;
