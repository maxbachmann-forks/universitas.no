import { connect } from 'react-redux'
import { getUser } from 'ducks/auth'
import { hot } from 'react-hot-loader'
import LoginForm2 from 'components/LoginForm'
import ProdSys from 'components/ProdSys'

import 'universitas/components/NewsFeed/NewsFeed.scss'
import 'universitas/styles/universitas.scss'
import 'styles/prodsys.scss'

// show loginform if the user is not authenticated
const ProdsysApp = ({ username, pending }) => {
  if (username) return <ProdSys />
  if (!pending) return <LoginForm2 />
  return null
}

// export as hot for react hot reload
export default hot(module)(connect(getUser)(ProdsysApp))
