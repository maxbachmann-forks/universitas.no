import { withErrorBoundary } from 'react-error-boundary'
import { Helmet } from 'react-helmet'
import { connect } from 'react-redux'
import { TransitionGroup, CSSTransition } from 'react-transition-group'
import { capitalize } from 'utils/text'
import cx from 'classnames'

import {
  HOME,
  SECTION,
  STORY,
  SHORT_URL,
  PDF,
  SCHEDULE,
  ABOUT,
  STYRE_INFO,
  AD_INFO,
  NOT_FOUND,
  getLocation,
} from 'universitas/ducks/router'
import { getSearch } from 'ducks/newsFeed'
import { NewsFeed, SearchFeed } from 'components/NewsFeed'
import Story from 'components/Story'
import PDFArchive from 'components/Pages/PDFArchive'
import PublicationSchedule from 'components/Pages/PublicationSchedule'
import AboutUniversitas from 'components/Pages/AboutUniversitas'
import AdvertiserInfo from 'components/Pages/AdvertiserInfo'
import PageNotFound from 'components/PageNotFound'
import StyreInfo from 'components/Pages/StyreInfo'

const PageHelmet = ({
  pageTitle = '',
  lede = 'Norges største studentavis',
  language = 'nb',
}) => {
  if (!pageTitle) return null
  const url = R.path(['location', 'href'], global)
  return (
    <Helmet>
      <title>{`${pageTitle} | universitas.no`}</title>
      <link rel="canonical" href={url} />
      <meta name="description" content={lede} />
      <meta property="og:type" content="website" />
      <meta property="og:title" content={pageTitle} />
      <meta property="og:description" content={lede} />
      <meta property="og:locale" content={language} />
      <meta property="og:url" content={url} />
    </Helmet>
  )
}

const onError = err => (window.__RENDER_ERROR__ = err || true)

const pageWrapper = (Page, toTitle = R.F) => {
  const title = R.pipe(
    toTitle,
    R.unless(R.is(String), R.always('')),
    R.trim,
    capitalize,
  )
  const locationToProps = R.pipe(
    R.converge(R.merge, [R.prop('payload'), R.pick(['pathname'])]),
    R.converge(R.assoc('pageTitle'), [title, R.identity]),
  )
  return [withErrorBoundary(Page, undefined, onError), locationToProps]
}

const pages = {
  [HOME]: pageWrapper(NewsFeed, R.always('Forsiden')),
  [SECTION]: pageWrapper(NewsFeed, R.prop('section')),
  [STORY]: pageWrapper(Story, R.prop('title')),
  [SHORT_URL]: pageWrapper(Story, R.prop('id')),
  [PDF]: pageWrapper(PDFArchive, ({ year = '' }) => `PDF-arkiv ${year}`),
  [SCHEDULE]: pageWrapper(
    PublicationSchedule,
    ({ year = '' }) => `Utgivelsesplan ${year}`,
  ),
  [ABOUT]: pageWrapper(AboutUniversitas, R.always('Om Universitas')),
  [STYRE_INFO]: pageWrapper(StyreInfo, R.always('Om Styret')),
  [AD_INFO]: pageWrapper(AdvertiserInfo, R.always('Annonsér i Universitas')),
  [NOT_FOUND]: pageWrapper(PageNotFound, R.always('ikke funnet (404)')),
}

const PageSwitch = ({ location = {}, search = '' }) => {
  const [PageComponent, locationToProps] = search
    ? [SearchFeed, R.identity]
    : pages[location.type] || pages[NOT_FOUND]
  const props = locationToProps(location)
  const key = R.contains(location.type, [SECTION, HOME])
    ? 'newsfeed' // Do not transition between feed pages.
    : location.pathname // ensure css transition
  return (
    <main className="PageSwitch">
      <PageHelmet {...props} />
      <TransitionGroup component={null}>
        <CSSTransition
          key={key}
          timeout={150}
          classNames="page"
          mountOnEnter
          unmountOnExit
        >
          <PageComponent className="Page" {...props} />
        </CSSTransition>
      </TransitionGroup>
    </main>
  )
}

export default connect(
  R.applySpec({ location: getLocation, search: getSearch }),
)(PageSwitch)
