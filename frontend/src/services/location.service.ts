const BASE_URL = 'https://provinces.open-api.vn/api'

export interface ProvinceOption {
  code: number
  name: string
  codename: string
  division_type: string
}

export interface DistrictOption {
  code: number
  name: string
  codename: string
  division_type: string
}

export interface WardOption {
  code: number
  name: string
  codename: string
  division_type: string
}

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `Request to ${url} failed with status ${res.status}`)
  }
  return res.json()
}

export const locationService = {
  async listProvinces(): Promise<ProvinceOption[]> {
    return fetchJson<ProvinceOption[]>(`${BASE_URL}/p/`)
  },

  async listDistricts(provinceCode: number): Promise<DistrictOption[]> {
    const data = await fetchJson<{ districts?: DistrictOption[] }>(`${BASE_URL}/p/${provinceCode}?depth=2`)
    return data.districts || []
  },

  async listWards(districtCode: number): Promise<WardOption[]> {
    const data = await fetchJson<{ wards?: WardOption[] }>(`${BASE_URL}/d/${districtCode}?depth=2`)
    return data.wards || []
  },
}
