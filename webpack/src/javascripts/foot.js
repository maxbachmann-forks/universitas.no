// wrap first few words in tingo paragraphs in inngangsord span.
import mount_react from './react'

const wrap_tingo = tingo => {
  const regex = /(^[^<]{0,10}[^\s<]*)/
  const replace = '<span class=inngangsord>$1</span>'
  tingo.innerHTML = tingo.innerHTML.replace(regex, replace)
}

document.querySelectorAll('p.tingo').forEach(wrap_tingo)
mount_react()
