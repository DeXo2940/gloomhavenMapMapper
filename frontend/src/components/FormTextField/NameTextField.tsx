import React from 'react';
import FormTextField from './FormTextField';

interface NameTextFieldProps {
  value: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  editable?: boolean;
  icon?: JSX.Element;
}

const NameTextField: React.FC<NameTextFieldProps> = ({ value, onChange, placeholder = '', editable = true, icon = <></> }) => {
  return (
    <FormTextField
      id='name'
      name='name'
      label='Name'
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      editable={editable}
      icon={icon}
    />
  );
}

export default NameTextField;
