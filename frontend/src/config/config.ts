export const apiUrl = 'http://localhost:5000'

export const idTemplate = ':id'

export const scenarioUrlSufix = '/scenarios'

export const scenarioUrlSufixIdTemplate = scenarioUrlSufix + '/' + idTemplate
export const scenarioUrlSufixId = (id: number) => scenarioUrlSufixIdTemplate.replace(idTemplate, id.toString())

export const scenarioUrl = apiUrl + scenarioUrlSufix

