import React from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import './App.scss';

import ExplorerRoutes from './explorer/ExplorerRoutes';

export default class App extends React.Component {
    render() {
        return (
            <>
                <BrowserRouter>
                    <Routes>
                        <Route path="/*" element={<ExplorerRoutes />}/>
                    </Routes>
                </BrowserRouter>
            </>
        );
    }
}