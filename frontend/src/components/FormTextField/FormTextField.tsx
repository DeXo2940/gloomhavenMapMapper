import React from 'react';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';

interface FormTextFieldProps {
    id: string;
    name: string;
    label: string;
    value: string;
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
    placeholder?: string;
    editable?: boolean;
    icon?: JSX.Element;
}
const FormTextField: React.FC<FormTextFieldProps> = ({ id, name, label, value, onChange, placeholder = '', editable = true, icon = <></> }) => {
    return (
        <TextField
            type="text"
            id={id}
            name={name}
            label={label}
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            disabled={!editable}
            fullWidth
            required
            InputProps={{ startAdornment: (<InputAdornment position="start">{icon}</InputAdornment>) }}
        />
    );
}

export default FormTextField;
