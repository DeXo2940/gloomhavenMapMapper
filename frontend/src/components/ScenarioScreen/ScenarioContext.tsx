import React, { createContext, useContext, useState } from 'react';

type ScenarioContextProps = {
    selectedScenarioId: string | null;
    setSelectedScenarioId: React.Dispatch<React.SetStateAction<string | null>>;
};

const ScenarioContext = createContext<ScenarioContextProps | undefined>(undefined);

export const ScenarioProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null);

    return (
        <ScenarioContext.Provider value={{ selectedScenarioId, setSelectedScenarioId }}>
            {children}
        </ScenarioContext.Provider>
    );
};

export const useScenarioContext = () => {
    const context = useContext(ScenarioContext);
    if (!context) {
        throw new Error('useScenarioContext must be used within a ScenarioProvider');
    }
    return context;
};
