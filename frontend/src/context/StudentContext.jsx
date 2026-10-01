import React, { createContext, useState } from "react";

export const studentDataContext = createContext();
export default function StudentContext({ children }) {
  const [student, setStudent] = useState(null);
  
  return (
    <div>
      <studentDataContext.Provider value={{ student, setStudent }}>
        {children}
      </studentDataContext.Provider>
    </div>
  );
}
