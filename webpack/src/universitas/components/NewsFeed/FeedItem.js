import cx from 'classnames'
import ErrorBoundary from 'react-error-boundary'
import Link from 'redux-first-router-link'
import { Done, Sync, Clear } from 'components/Icons'
import { toStory } from 'ducks/router'
import { hyphenate, slugify } from 'utils/text'
import { renderStyles, parseStyles } from './feedItemStyles.js'

const position = ({ x = 0.5, y = 0.5 }) => `${x * 100}% ${y * 100}%`

const ifChildren = Component => props =>
  props.children ? <Component {...props} /> : null

const Vignette = ifChildren(({ children, sectionName }) => (
  <div className="Vignette">
    <div className="bg-section">{children}</div>
  </div>
))
const Headline = ifChildren(({ children }) => (
  <h1 className="Headline">{children}</h1>
))
const Kicker = ifChildren(({ children }) => (
  <h3 className="Kicker">{children}</h3>
))
const Lede = ifChildren(({ children }) => <p className="Lede">{children}</p>)

const FeedImage = ({ image, crop_box }) =>
  image ? (
    <div
      className="FeedImage"
      style={{
        backgroundRepeat: 'none',
        backgroundImage: `url(${image})`,
        backgroundPosition: position(crop_box),
        backgroundSize: 'cover',
        height: '100%',
      }}
    />
  ) : null

const Wrapper = props => <div {...props} />

export const FeedItem = ({
  html_class,
  size: [columns, rows] = [2, 2],
  image,
  headline,
  vignette,
  kicker,
  lede,
  crop_box,
  sectionName = '',
  className,
  Wrapper = Wrapper,
  ...props
}) => (
  <Wrapper
    className={cx(
      className,
      'FeedItem',
      `col-${columns}`,
      `row-${rows}`,
      `section-${slugify(sectionName)}`,
      renderStyles(parseStyles(html_class)),
    )}
    {...props}
  >
    <FeedImage image={image} crop_box={crop_box} />
    <Vignette>{vignette}</Vignette>
    <Kicker>{hyphenate(kicker)}</Kicker>
    <Headline>{hyphenate(headline)}</Headline>
    <Lede>{lede}</Lede>
  </Wrapper>
)

const LinkWrapper = ({ fetchStatus, story, addRef, children, className }) => {
  return (
    <Link to={toStory(story)} className={className}>
      <ErrorBoundary>
        {children}
        {addRef && <div style={{ gridArea: '1/1' }} ref={addRef(story.id)} />}
      </ErrorBoundary>
    </Link>
  )
}

export default props => <FeedItem {...props} Wrapper={LinkWrapper} />
