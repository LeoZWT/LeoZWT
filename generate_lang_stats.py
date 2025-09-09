#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Language Statistics Generator
动态生成GitHub语言统计SVG，支持私有仓库
"""

import requests
import json
import os
from collections import defaultdict
from typing import Dict, List, Tuple
from dotenv import load_dotenv

class GitHubLangStats:
    def __init__(self, token: str, username: str):
        self.token = token
        self.username = username
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
    
    def get_all_repositories(self) -> List[Dict]:
        """获取用户所有仓库（包括私有）"""
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f'{self.base_url}/user/repos'
            params = {
                'page': page,
                'per_page': per_page,
                'type': 'all',  # 包括私有仓库
                'sort': 'updated',
                'direction': 'desc'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"Error fetching repositories: {response.status_code}")
                break
            
            page_repos = response.json()
            if not page_repos:
                break
            
            repos.extend(page_repos)
            page += 1
            
            # GitHub API限制，避免过多请求
            if len(repos) >= 1000:
                break
        
        return repos
    
    def get_repository_languages(self, repo_name: str) -> Dict[str, int]:
        """获取单个仓库的语言统计"""
        url = f'{self.base_url}/repos/{self.username}/{repo_name}/languages'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching languages for {repo_name}: {response.status_code}")
            return {}
    
    def calculate_language_stats(self) -> Dict[str, int]:
        """计算所有仓库的语言统计"""
        print("正在获取仓库列表...")
        repos = self.get_all_repositories()
        print(f"找到 {len(repos)} 个仓库")
        
        language_stats = defaultdict(int)
        
        for i, repo in enumerate(repos, 1):
            repo_name = repo['name']
            print(f"处理仓库 {i}/{len(repos)}: {repo_name}")
            
            languages = self.get_repository_languages(repo_name)
            for lang, bytes_count in languages.items():
                language_stats[lang] += bytes_count
        
        return dict(language_stats)
    
    def get_top_languages(self, limit: int = 6) -> List[Tuple[str, float]]:
        """获取使用最多的编程语言"""
        stats = self.calculate_language_stats()
        total_bytes = sum(stats.values())
        
        if total_bytes == 0:
            return []
        
        # 计算百分比并排序
        lang_percentages = [(lang, (bytes_count / total_bytes) * 100) 
                           for lang, bytes_count in stats.items()]
        lang_percentages.sort(key=lambda x: x[1], reverse=True)
        
        return lang_percentages[:limit]
    
    def generate_svg(self, output_path: str = 'assets/lang-stats-dynamic.svg'):
        """生成动态语言统计SVG"""
        print("正在生成语言统计...")
        top_languages = self.get_top_languages()
        
        if not top_languages:
            print("未找到语言数据")
            return
        
        # 语言颜色映射
        language_colors = {
            'Python': ('#3776ab', '#ffd43b'),
            'Julia': ('#f7df1e', '#323330'),
            'Fortarn': ('#3178c6', '#ffffff'),
            'C++': ('#00599c', '#004482'),
            'Java': ('#ed8b00', '#5382a1'),
            'C': ('#a8b9cc', '#283593'),
            'HTML': ('#e34f26', '#f06529'),
            'CSS': ('#1572b6', '#33a9dc'),
            'Shell': ('#89e051', '#4eaa25'),
            'Go': ('#00add8', '#7fd3ed'),
            'Rust': ('#dea584', '#ce422b'),
            'PHP': ('#777bb4', '#8892bf'),
            'Ruby': ('#cc342d', '#701516'),
            'Swift': ('#fa7343', '#ffac45'),
            'Kotlin': ('#7f52ff', '#a97bff'),
            'Dart': ('#00b4ab', '#01579b')
        }
        
        svg_content = self._create_svg_template(top_languages, language_colors)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"SVG已生成: {output_path}")
        
        # 打印统计结果
        print("\n语言统计结果:")
        for lang, percentage in top_languages:
            print(f"  {lang}: {percentage:.1f}%")
    
    def _create_svg_template(self, languages: List[Tuple[str, float]], colors: Dict) -> str:
        """创建SVG模板"""
        svg_header = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="{height}" viewBox="0 0 400 {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Programming Languages Statistics</title>
  <desc id="desc">Dynamic language statistics with breathing light effect</desc>
  
  <defs>
    <!-- Breathing gradient -->
    <radialGradient id="breathingGradient" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00E1FF" stop-opacity="0.8">
        <animate attributeName="stop-opacity" values="0.3;0.9;0.3" dur="3s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="#7A5CFF" stop-opacity="0.6">
        <animate attributeName="stop-opacity" values="0.2;0.8;0.2" dur="3s" begin="0.5s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#FF4D8D" stop-opacity="0.4">
        <animate attributeName="stop-opacity" values="0.1;0.7;0.1" dur="3s" begin="1s" repeatCount="indefinite"/>
      </stop>
    </radialGradient>
    
    <!-- Text glow filter -->
    <filter id="textGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>'''
        
        # 动态生成语言渐变
        gradients = []
        for i, (lang, _) in enumerate(languages):
            if lang in colors:
                color1, color2 = colors[lang]
                gradients.append(f'''
    <linearGradient id="{lang.lower()}Grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{color1}"/>
      <stop offset="100%" stop-color="{color2}"/>
    </linearGradient>''')
            else:
                # 默认渐变
                gradients.append(f'''
    <linearGradient id="{lang.lower()}Grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#58a6ff"/>
      <stop offset="100%" stop-color="#1f6feb"/>
    </linearGradient>''')
        
        height = 120 + len(languages) * 40
        
        svg_body = f'''
  </defs>
  
  <!-- Background with breathing effect -->
  <rect width="100%" height="100%" fill="url(#breathingGradient)" opacity="0.1"/>
  
  <!-- Border with breathing effect -->
  <rect x="2" y="2" width="396" height="{height-4}" fill="none" stroke="#30363d" stroke-width="2" rx="6">
    <animate attributeName="stroke-opacity" values="0.3;0.8;0.3" dur="4s" repeatCount="indefinite"/>
  </rect>
  
  <!-- Title -->
  <text x="200" y="30" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="600" text-anchor="middle" fill="#c9d1d9" filter="url(#textGlow)">
    Most Used Languages
    <animate attributeName="opacity" values="0.7;1;0.7" dur="2.5s" repeatCount="indefinite"/>
  </text>
  
  <!-- Language bars -->
  <g transform="translate(30, 60)">'''
        
        # 生成语言条
        language_bars = []
        for i, (lang, percentage) in enumerate(languages):
            y_offset = i * 40
            bar_width = int((percentage / 100) * 300)
            delay = 0.5 + i * 0.5
            breathing_delay = 2.5 + i * 0.5
            
            language_bars.append(f'''
    <!-- {lang} -->
    <g transform="translate(0, {y_offset})">
      <text x="0" y="15" font-family="'Segoe UI', sans-serif" font-size="12" fill="#c9d1d9">{lang}</text>
      <text x="340" y="15" font-family="'Segoe UI', sans-serif" font-size="12" fill="#8b949e">{percentage:.1f}%</text>
      <rect x="0" y="20" width="300" height="8" fill="#21262d" rx="4"/>
      <rect x="0" y="20" width="0" height="8" fill="url(#{lang.lower()}Grad)" rx="4">
        <animate attributeName="width" values="0;{bar_width}" dur="2s" begin="{delay}s" fill="freeze"/>
        <animate attributeName="opacity" values="0.6;1;0.6" dur="3s" begin="{breathing_delay}s" repeatCount="indefinite"/>
      </rect>
    </g>''')
        
        svg_footer = f'''
  </g>
  
  <!-- Footer text with breathing effect -->
  <text x="200" y="{height-20}" font-family="'Segoe UI', sans-serif" font-size="10" text-anchor="middle" fill="#8b949e">
    Updated dynamically from GitHub API
    <animate attributeName="opacity" values="0.4;0.9;0.4" dur="4s" repeatCount="indefinite"/>
  </text>
</svg>'''
        
        return (svg_header.format(height=height) + 
                ''.join(gradients) + 
                svg_body + 
                ''.join(language_bars) + 
                svg_footer)

def main():
    # 加载.env文件
    load_dotenv()
    
    # 从环境变量获取GitHub token
    token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_USERNAME', 'LeoZWT')
    output_path = os.getenv('OUTPUT_PATH', 'assets/lang-stats-dynamic.svg')
    
    if not token:
        print("错误: 请设置GITHUB_TOKEN环境变量")
        print("获取token: https://github.com/settings/tokens")
        print("需要权限: repo (访问私有仓库)")
        return
    
    generator = GitHubLangStats(token, username)
    generator.generate_svg(output_path)

if __name__ == '__main__':
    main()