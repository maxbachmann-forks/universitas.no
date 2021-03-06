// helpers for file inputs and upload
import slugify from 'slugify'

// :: str -> bool
const isObjectURL = str => R.match(/^blob:https?\/\//)

// Turn serializable data into FormData. Fetches any object URLs
// :: object -> FormData
export const jsonToFormData = obj => {
  const form = new FormData()
  R.forEachObjIndexed((val, key) => form.set(key, val), obj)
  return form
}

export const objectURLtoFile = (url, filename) =>
  fetch(url)
    .then(r => r.blob())
    .then(b => new File([b], filename))

export const slugifyFilename = ({ filename, mimetype }) => {
  const ext = R.pipe(
    R.split('/'),
    R.last,
    R.replace('jpeg', 'jpg'),
  )
  const stem = R.pipe(
    R.trim,
    R.replace(/\.[^.]{0,4}$/, ''),
    slugify,
    R.replace(/[^a-z0-9]+/gi, ' '),
    R.trim,
    R.replace(/\s+/g, '-'),
  )
  //const zeroPad = (n, pad = '00') => (pad + n).slice(-pad.length)
  return stem(filename) + '.' + ext(mimetype)
}
