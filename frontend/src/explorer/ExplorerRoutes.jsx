import React from 'react'
import { Routes, Route } from 'react-router-dom';

import BlockchainView from './views/BlockchainView';

class ExplorerRoutes extends React.Component {
    render() {
        return (
            <Routes>
                <Route path="/*" element={<BlockchainView />}/>
                {/*Route path={`${path}/report/:id`} component={ReportView}/>*/}
            </Routes>
        )
    }
}

export default ExplorerRoutes;