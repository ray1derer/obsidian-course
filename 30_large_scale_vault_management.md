# 제30강: 대규모 볼트 관리

## 학습 목표
- 수천 개 노트의 효율적 관리 전략
- 성능 최적화 및 인덱싱 기법
- 볼트 구조 설계 및 리팩토링
- 백업 및 복구 전략
- 대규모 팀 협업 관리

## 1. 대규모 볼트의 이해

### 1.1 대규모 볼트의 특징과 과제
```markdown
# 대규모 볼트의 정의

## 규모별 분류
### 소규모 (< 1,000개 노트)
- 개인 사용 중심
- 단순한 폴더 구조
- 수동 관리 가능

### 중규모 (1,000 - 10,000개 노트)
- 체계적 구조 필요
- 자동화 도입 필요
- 검색 최적화 중요

### 대규모 (10,000 - 100,000개 노트)
- 전문적 관리 필수
- 성능 최적화 핵심
- 팀 협업 고려

### 초대규모 (> 100,000개 노트)
- 엔터프라이즈 수준
- 분산 시스템 고려
- 전용 인프라 필요

## 주요 과제
1. **성능 저하**
   - 검색 속도 감소
   - 인덱싱 시간 증가
   - UI 반응성 저하

2. **관리 복잡성**
   - 중복 콘텐츠
   - 구조 일관성
   - 명명 규칙

3. **협업 문제**
   - 동시 편집
   - 권한 관리
   - 버전 충돌

4. **기술적 한계**
   - 메모리 사용
   - 파일 시스템 제한
   - 동기화 문제
```

### 1.2 확장 가능한 아키텍처
```javascript
// 대규모 볼트 아키텍처
class ScalableVaultArchitecture {
  constructor() {
    this.config = {
      maxNodesPerFolder: 1000,
      indexBatchSize: 100,
      cacheSize: 10000,
      shardingEnabled: true,
      compressionEnabled: true
    };
    
    this.structure = new VaultStructure();
    this.indexer = new AdvancedIndexer();
    this.cache = new HierarchicalCache();
    this.monitor = new PerformanceMonitor();
  }

  // 볼트 초기화
  async initialize(vaultPath) {
    console.log('Initializing scalable vault architecture...');
    
    // 1. 구조 분석
    const analysis = await this.analyzeVaultStructure(vaultPath);
    
    // 2. 최적화 제안
    const optimizations = this.suggestOptimizations(analysis);
    
    // 3. 구조 재구성
    if (optimizations.restructureNeeded) {
      await this.restructureVault(vaultPath, optimizations);
    }
    
    // 4. 인덱싱 시작
    await this.indexer.buildIndex(vaultPath);
    
    // 5. 캐시 초기화
    await this.cache.initialize();
    
    // 6. 모니터링 시작
    this.monitor.start();
    
    return {
      structure: analysis,
      optimizations: optimizations,
      performance: await this.monitor.getBaseline()
    };
  }

  // 볼트 구조 분석
  async analyzeVaultStructure(vaultPath) {
    const analysis = {
      totalFiles: 0,
      totalFolders: 0,
      maxDepth: 0,
      largestFolder: { path: '', count: 0 },
      fileDistribution: new Map(),
      sizeDistribution: new Map(),
      typeDistribution: new Map(),
      issues: []
    };

    const traverse = async (path, depth = 0) => {
      const items = await this.getItems(path);
      
      analysis.totalFolders++;
      analysis.maxDepth = Math.max(analysis.maxDepth, depth);
      
      const fileCount = items.filter(i => i.type === 'file').length;
      if (fileCount > analysis.largestFolder.count) {
        analysis.largestFolder = { path, count: fileCount };
      }
      
      // 파일 분포 분석
      analysis.fileDistribution.set(path, fileCount);
      
      for (const item of items) {
        if (item.type === 'file') {
          analysis.totalFiles++;
          
          // 크기 분포
          const sizeCategory = this.getSizeCategory(item.size);
          const currentCount = analysis.sizeDistribution.get(sizeCategory) || 0;
          analysis.sizeDistribution.set(sizeCategory, currentCount + 1);
          
          // 타입 분포
          const type = item.extension || 'no-extension';
          const typeCount = analysis.typeDistribution.get(type) || 0;
          analysis.typeDistribution.set(type, typeCount + 1);
          
        } else if (item.type === 'folder') {
          await traverse(item.path, depth + 1);
        }
      }
      
      // 문제점 감지
      if (fileCount > this.config.maxNodesPerFolder) {
        analysis.issues.push({
          type: 'too-many-files',
          path,
          count: fileCount,
          severity: 'high'
        });
      }
    };

    await traverse(vaultPath);
    
    // 추가 분석
    analysis.averageFilesPerFolder = analysis.totalFiles / analysis.totalFolders;
    analysis.recommendedSharding = analysis.totalFiles > 10000;
    
    return analysis;
  }

  // 최적화 제안
  suggestOptimizations(analysis) {
    const suggestions = {
      restructureNeeded: false,
      actions: [],
      estimatedImprovement: 0
    };

    // 폴더당 파일 수 확인
    if (analysis.largestFolder.count > this.config.maxNodesPerFolder) {
      suggestions.restructureNeeded = true;
      suggestions.actions.push({
        type: 'split-folder',
        target: analysis.largestFolder.path,
        reason: 'Too many files in single folder',
        strategy: 'alphabetical-sharding'
      });
      suggestions.estimatedImprovement += 30;
    }

    // 깊이 확인
    if (analysis.maxDepth > 7) {
      suggestions.actions.push({
        type: 'flatten-structure',
        reason: 'Directory tree too deep',
        strategy: 'selective-flattening'
      });
      suggestions.estimatedImprovement += 15;
    }

    // 파일 크기 최적화
    const largeFiles = Array.from(analysis.sizeDistribution.entries())
      .filter(([category]) => category === 'large' || category === 'huge');
    
    if (largeFiles.length > 0) {
      suggestions.actions.push({
        type: 'optimize-large-files',
        count: largeFiles.reduce((sum, [, count]) => sum + count, 0),
        strategy: 'compression-and-archiving'
      });
      suggestions.estimatedImprovement += 20;
    }

    // 샤딩 제안
    if (analysis.recommendedSharding) {
      suggestions.actions.push({
        type: 'enable-sharding',
        reason: 'Large number of files',
        strategy: 'content-based-sharding'
      });
      suggestions.estimatedImprovement += 25;
    }

    return suggestions;
  }

  // 볼트 재구성
  async restructureVault(vaultPath, optimizations) {
    console.log('Starting vault restructuring...');
    
    for (const action of optimizations.actions) {
      switch (action.type) {
        case 'split-folder':
          await this.splitLargeFolder(action.target, action.strategy);
          break;
          
        case 'flatten-structure':
          await this.flattenDeepStructure(vaultPath, action.strategy);
          break;
          
        case 'optimize-large-files':
          await this.optimizeLargeFiles(vaultPath);
          break;
          
        case 'enable-sharding':
          await this.enableSharding(vaultPath, action.strategy);
          break;
      }
    }
    
    console.log('Vault restructuring complete');
  }

  // 대용량 폴더 분할
  async splitLargeFolder(folderPath, strategy) {
    const items = await this.getItems(folderPath);
    const files = items.filter(i => i.type === 'file');
    
    if (strategy === 'alphabetical-sharding') {
      // 알파벳별 분할
      const shards = new Map();
      
      for (const file of files) {
        const firstChar = file.name[0].toUpperCase();
        const shardKey = /[A-Z]/.test(firstChar) ? firstChar : '#';
        
        if (!shards.has(shardKey)) {
          shards.set(shardKey, []);
        }
        shards.get(shardKey).push(file);
      }
      
      // 샤드 폴더 생성 및 파일 이동
      for (const [shard, shardFiles] of shards) {
        const shardPath = `${folderPath}/${shard}`;
        await this.createFolder(shardPath);
        
        for (const file of shardFiles) {
          await this.moveFile(file.path, `${shardPath}/${file.name}`);
        }
      }
    }
  }

  getSizeCategory(size) {
    if (size < 10 * 1024) return 'tiny';           // < 10KB
    if (size < 100 * 1024) return 'small';         // < 100KB
    if (size < 1024 * 1024) return 'medium';       // < 1MB
    if (size < 10 * 1024 * 1024) return 'large';   // < 10MB
    return 'huge';                                   // >= 10MB
  }
}

// 고급 인덱서
class AdvancedIndexer {
  constructor() {
    this.index = {
      content: new InvertedIndex(),
      metadata: new MetadataIndex(),
      links: new LinkGraph(),
      tags: new TagIndex()
    };
    
    this.config = {
      batchSize: 100,
      workerThreads: 4,
      incrementalUpdate: true,
      compressionEnabled: true
    };
  }

  // 인덱스 구축
  async buildIndex(vaultPath) {
    console.log('Building advanced index...');
    
    const files = await this.getAllFiles(vaultPath);
    const batches = this.createBatches(files, this.config.batchSize);
    
    // 워커 스레드 사용
    const workers = this.createWorkers();
    const results = [];
    
    for (let i = 0; i < batches.length; i++) {
      const workerIndex = i % workers.length;
      const result = await workers[workerIndex].process(batches[i]);
      results.push(result);
      
      // 진행률 표시
      const progress = ((i + 1) / batches.length * 100).toFixed(1);
      console.log(`Indexing progress: ${progress}%`);
    }
    
    // 결과 병합
    await this.mergeResults(results);
    
    // 인덱스 최적화
    await this.optimizeIndex();
    
    // 인덱스 저장
    await this.saveIndex();
    
    console.log('Index building complete');
  }

  // 워커 생성
  createWorkers() {
    const workers = [];
    
    for (let i = 0; i < this.config.workerThreads; i++) {
      workers.push(new IndexWorker());
    }
    
    return workers;
  }

  // 배치 생성
  createBatches(items, batchSize) {
    const batches = [];
    
    for (let i = 0; i < items.length; i += batchSize) {
      batches.push(items.slice(i, i + batchSize));
    }
    
    return batches;
  }

  // 결과 병합
  async mergeResults(results) {
    for (const result of results) {
      // 콘텐츠 인덱스 병합
      this.index.content.merge(result.content);
      
      // 메타데이터 인덱스 병합
      this.index.metadata.merge(result.metadata);
      
      // 링크 그래프 병합
      this.index.links.merge(result.links);
      
      // 태그 인덱스 병합
      this.index.tags.merge(result.tags);
    }
  }

  // 인덱스 최적화
  async optimizeIndex() {
    // 콘텐츠 인덱스 압축
    if (this.config.compressionEnabled) {
      await this.index.content.compress();
    }
    
    // 링크 그래프 최적화
    await this.index.links.calculatePageRank();
    
    // 태그 클러스터링
    await this.index.tags.cluster();
  }

  // 증분 업데이트
  async updateIncremental(changes) {
    for (const change of changes) {
      switch (change.type) {
        case 'created':
          await this.indexFile(change.file);
          break;
          
        case 'modified':
          await this.reindexFile(change.file);
          break;
          
        case 'deleted':
          await this.removeFromIndex(change.file);
          break;
      }
    }
  }
}

// 인덱스 워커
class IndexWorker {
  async process(files) {
    const result = {
      content: new Map(),
      metadata: new Map(),
      links: [],
      tags: new Map()
    };
    
    for (const file of files) {
      const content = await this.readFile(file);
      
      // 콘텐츠 인덱싱
      const tokens = this.tokenize(content);
      result.content.set(file.path, tokens);
      
      // 메타데이터 추출
      const metadata = this.extractMetadata(content);
      result.metadata.set(file.path, metadata);
      
      // 링크 추출
      const links = this.extractLinks(content);
      result.links.push(...links.map(link => ({
        source: file.path,
        target: link
      })));
      
      // 태그 추출
      const tags = this.extractTags(content);
      tags.forEach(tag => {
        if (!result.tags.has(tag)) {
          result.tags.set(tag, []);
        }
        result.tags.get(tag).push(file.path);
      });
    }
    
    return result;
  }

  tokenize(content) {
    // 고급 토큰화
    return content
      .toLowerCase()
      .replace(/[^\w\s가-힣]/g, ' ')
      .split(/\s+/)
      .filter(token => token.length > 2);
  }

  extractMetadata(content) {
    const metadata = {};
    
    // YAML frontmatter 추출
    const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (yamlMatch) {
      // YAML 파싱 (실제 구현에서는 yaml 라이브러리 사용)
      const yamlContent = yamlMatch[1];
      const lines = yamlContent.split('\n');
      
      lines.forEach(line => {
        const [key, value] = line.split(':').map(s => s.trim());
        if (key && value) {
          metadata[key] = value;
        }
      });
    }
    
    return metadata;
  }

  extractLinks(content) {
    const links = [];
    const linkRegex = /\[\[([^\]]+)\]\]/g;
    
    let match;
    while ((match = linkRegex.exec(content)) !== null) {
      links.push(match[1]);
    }
    
    return links;
  }

  extractTags(content) {
    const tags = new Set();
    const tagRegex = /#[\w가-힣]+/g;
    
    let match;
    while ((match = tagRegex.exec(content)) !== null) {
      tags.add(match[0]);
    }
    
    return Array.from(tags);
  }

  async readFile(file) {
    // 실제 구현에서는 파일 시스템 API 사용
    return file.content || '';
  }
}
```

## 2. 성능 최적화

### 2.1 인덱싱 최적화
```javascript
// 고성능 검색 엔진
class HighPerformanceSearchEngine {
  constructor() {
    this.indices = {
      primary: new PrimaryIndex(),
      secondary: new SecondaryIndex(),
      fullText: new FullTextIndex(),
      semantic: new SemanticIndex()
    };
    
    this.cache = new MultiLevelCache();
    this.queryOptimizer = new QueryOptimizer();
  }

  // 검색 실행
  async search(query, options = {}) {
    const startTime = performance.now();
    
    // 캐시 확인
    const cacheKey = this.getCacheKey(query, options);
    const cached = await this.cache.get(cacheKey);
    
    if (cached && !options.noCache) {
      return {
        results: cached.results,
        fromCache: true,
        duration: performance.now() - startTime
      };
    }
    
    // 쿼리 최적화
    const optimizedQuery = await this.queryOptimizer.optimize(query);
    
    // 검색 전략 선택
    const strategy = this.selectSearchStrategy(optimizedQuery, options);
    
    // 검색 실행
    const results = await this.executeSearch(optimizedQuery, strategy);
    
    // 결과 정렬 및 필터링
    const processed = await this.processResults(results, options);
    
    // 캐시 저장
    await this.cache.set(cacheKey, {
      results: processed,
      timestamp: Date.now()
    });
    
    return {
      results: processed,
      fromCache: false,
      duration: performance.now() - startTime,
      strategy: strategy.name
    };
  }

  // 검색 전략 선택
  selectSearchStrategy(query, options) {
    const strategies = {
      exact: {
        name: 'exact-match',
        indices: ['primary'],
        weight: 1.0
      },
      fuzzy: {
        name: 'fuzzy-search',
        indices: ['primary', 'secondary'],
        weight: 0.8
      },
      fullText: {
        name: 'full-text',
        indices: ['fullText'],
        weight: 0.7
      },
      semantic: {
        name: 'semantic',
        indices: ['semantic'],
        weight: 0.9
      },
      hybrid: {
        name: 'hybrid',
        indices: ['primary', 'fullText', 'semantic'],
        weight: 0.85
      }
    };
    
    // 쿼리 특성에 따른 전략 선택
    if (query.type === 'exact') return strategies.exact;
    if (query.type === 'semantic') return strategies.semantic;
    if (options.fast) return strategies.exact;
    
    // 기본 전략
    return strategies.hybrid;
  }

  // 검색 실행
  async executeSearch(query, strategy) {
    const results = new Map();
    
    // 병렬 검색
    const searches = strategy.indices.map(indexName => 
      this.searchIndex(indexName, query)
    );
    
    const indexResults = await Promise.all(searches);
    
    // 결과 병합
    indexResults.forEach((result, index) => {
      const indexName = strategy.indices[index];
      
      result.forEach(item => {
        const existing = results.get(item.id) || {
          id: item.id,
          scores: {},
          data: item.data
        };
        
        existing.scores[indexName] = item.score;
        results.set(item.id, existing);
      });
    });
    
    // 종합 점수 계산
    const scored = Array.from(results.values()).map(item => ({
      ...item,
      totalScore: this.calculateTotalScore(item.scores, strategy)
    }));
    
    // 정렬
    return scored.sort((a, b) => b.totalScore - a.totalScore);
  }

  // 인덱스별 검색
  async searchIndex(indexName, query) {
    const index = this.indices[indexName];
    return await index.search(query);
  }

  // 종합 점수 계산
  calculateTotalScore(scores, strategy) {
    let total = 0;
    const weights = {
      primary: 1.0,
      secondary: 0.7,
      fullText: 0.8,
      semantic: 0.9
    };
    
    Object.entries(scores).forEach(([index, score]) => {
      total += score * weights[index] * strategy.weight;
    });
    
    return total;
  }

  // 결과 처리
  async processResults(results, options) {
    let processed = results;
    
    // 필터링
    if (options.filters) {
      processed = this.applyFilters(processed, options.filters);
    }
    
    // 페이징
    if (options.limit) {
      const start = (options.page || 0) * options.limit;
      processed = processed.slice(start, start + options.limit);
    }
    
    // 하이라이팅
    if (options.highlight) {
      processed = await this.addHighlights(processed, options.query);
    }
    
    return processed;
  }
}

// 다단계 캐시
class MultiLevelCache {
  constructor() {
    this.levels = [
      new MemoryCache({ size: 1000, ttl: 60000 }),      // L1: 1분
      new DiskCache({ size: 10000, ttl: 3600000 }),     // L2: 1시간
      new CompressedCache({ size: 100000, ttl: 86400000 }) // L3: 24시간
    ];
  }

  async get(key) {
    for (let i = 0; i < this.levels.length; i++) {
      const value = await this.levels[i].get(key);
      
      if (value) {
        // 상위 레벨에 복사
        for (let j = 0; j < i; j++) {
          await this.levels[j].set(key, value);
        }
        
        return value;
      }
    }
    
    return null;
  }

  async set(key, value) {
    // 모든 레벨에 저장
    await Promise.all(
      this.levels.map(cache => cache.set(key, value))
    );
  }

  // 캐시 통계
  getStats() {
    return this.levels.map((cache, index) => ({
      level: `L${index + 1}`,
      ...cache.getStats()
    }));
  }
}

// 메모리 캐시
class MemoryCache {
  constructor(options) {
    this.cache = new Map();
    this.options = options;
    this.stats = {
      hits: 0,
      misses: 0,
      evictions: 0
    };
  }

  async get(key) {
    const entry = this.cache.get(key);
    
    if (!entry) {
      this.stats.misses++;
      return null;
    }
    
    // TTL 확인
    if (Date.now() - entry.timestamp > this.options.ttl) {
      this.cache.delete(key);
      this.stats.misses++;
      return null;
    }
    
    this.stats.hits++;
    return entry.value;
  }

  async set(key, value) {
    // 크기 제한 확인
    if (this.cache.size >= this.options.size) {
      this.evictOldest();
    }
    
    this.cache.set(key, {
      value,
      timestamp: Date.now()
    });
  }

  evictOldest() {
    const oldest = Array.from(this.cache.entries())
      .sort((a, b) => a[1].timestamp - b[1].timestamp)[0];
    
    if (oldest) {
      this.cache.delete(oldest[0]);
      this.stats.evictions++;
    }
  }

  getStats() {
    const total = this.stats.hits + this.stats.misses;
    
    return {
      ...this.stats,
      hitRate: total > 0 ? (this.stats.hits / total * 100).toFixed(2) + '%' : '0%',
      size: this.cache.size,
      maxSize: this.options.size
    };
  }
}
```

### 2.2 메모리 관리
```javascript
// 메모리 관리자
class MemoryManager {
  constructor() {
    this.pools = new Map();
    this.monitors = new Map();
    this.limits = {
      total: 4 * 1024 * 1024 * 1024, // 4GB
      perPool: 512 * 1024 * 1024,    // 512MB
      warning: 0.8,                   // 80%
      critical: 0.95                  // 95%
    };
  }

  // 메모리 풀 생성
  createPool(name, config = {}) {
    const pool = new MemoryPool({
      name,
      size: config.size || this.limits.perPool,
      growable: config.growable !== false,
      maxGrowth: config.maxGrowth || 2
    });
    
    this.pools.set(name, pool);
    this.monitors.set(name, new MemoryMonitor(pool));
    
    return pool;
  }

  // 메모리 할당
  async allocate(poolName, size) {
    const pool = this.pools.get(poolName);
    if (!pool) throw new Error(`Pool not found: ${poolName}`);
    
    // 메모리 압력 확인
    const pressure = await this.getMemoryPressure();
    
    if (pressure > this.limits.critical) {
      // 긴급 GC
      await this.emergencyGC();
    } else if (pressure > this.limits.warning) {
      // 선택적 GC
      await this.selectiveGC();
    }
    
    // 할당 시도
    try {
      return await pool.allocate(size);
    } catch (error) {
      if (error.code === 'ENOMEM') {
        // 메모리 부족 처리
        await this.handleOutOfMemory(poolName, size);
        
        // 재시도
        return await pool.allocate(size);
      }
      
      throw error;
    }
  }

  // 메모리 압력 계산
  async getMemoryPressure() {
    const usage = process.memoryUsage();
    const total = this.limits.total;
    
    return (usage.heapUsed + usage.external) / total;
  }

  // 긴급 가비지 컬렉션
  async emergencyGC() {
    console.warn('Emergency GC triggered');
    
    // 모든 풀에서 사용하지 않는 메모리 해제
    for (const [name, pool] of this.pools) {
      await pool.compact();
    }
    
    // 캐시 비우기
    await this.clearCaches();
    
    // 강제 GC
    if (global.gc) {
      global.gc();
    }
  }

  // 선택적 가비지 컬렉션
  async selectiveGC() {
    // 사용률이 낮은 풀부터 정리
    const poolStats = Array.from(this.pools.entries())
      .map(([name, pool]) => ({
        name,
        pool,
        usage: pool.getUsage()
      }))
      .sort((a, b) => a.usage - b.usage);
    
    for (const { pool } of poolStats.slice(0, 3)) {
      await pool.compact();
    }
  }

  // OOM 처리
  async handleOutOfMemory(poolName, requestedSize) {
    console.error(`Out of memory in pool: ${poolName}, requested: ${requestedSize}`);
    
    // 1. 다른 풀에서 메모리 회수
    await this.reclaimMemoryFromOtherPools(poolName);
    
    // 2. 임시 파일로 스왑
    await this.swapToFile(poolName);
    
    // 3. 풀 크기 확장 (가능한 경우)
    const pool = this.pools.get(poolName);
    if (pool.config.growable) {
      await pool.grow();
    }
  }

  // 메모리 모니터링 리포트
  getMemoryReport() {
    const report = {
      timestamp: new Date(),
      system: process.memoryUsage(),
      pools: {},
      warnings: []
    };
    
    for (const [name, pool] of this.pools) {
      const stats = pool.getStats();
      report.pools[name] = stats;
      
      if (stats.usage > this.limits.warning) {
        report.warnings.push({
          pool: name,
          usage: stats.usage,
          message: 'High memory usage'
        });
      }
    }
    
    return report;
  }
}

// 메모리 풀
class MemoryPool {
  constructor(config) {
    this.config = config;
    this.allocated = new Map();
    this.free = [];
    this.totalSize = config.size;
    this.usedSize = 0;
  }

  async allocate(size) {
    if (this.usedSize + size > this.totalSize) {
      throw new Error('ENOMEM');
    }
    
    const buffer = Buffer.allocUnsafe(size);
    const id = crypto.randomUUID();
    
    this.allocated.set(id, {
      buffer,
      size,
      timestamp: Date.now()
    });
    
    this.usedSize += size;
    
    return { id, buffer };
  }

  async free(id) {
    const allocation = this.allocated.get(id);
    if (!allocation) return;
    
    this.allocated.delete(id);
    this.usedSize -= allocation.size;
    
    // 재사용을 위해 free 리스트에 추가
    if (allocation.size <= 1024 * 1024) { // 1MB 이하만
      this.free.push({
        buffer: allocation.buffer,
        size: allocation.size
      });
    }
  }

  async compact() {
    // 오래된 할당 해제
    const now = Date.now();
    const maxAge = 60 * 60 * 1000; // 1시간
    
    for (const [id, allocation] of this.allocated) {
      if (now - allocation.timestamp > maxAge) {
        await this.free(id);
      }
    }
    
    // free 리스트 정리
    this.free = this.free.slice(-100); // 최근 100개만 유지
  }

  getStats() {
    return {
      totalSize: this.totalSize,
      usedSize: this.usedSize,
      freeSize: this.totalSize - this.usedSize,
      usage: (this.usedSize / this.totalSize * 100).toFixed(2) + '%',
      allocations: this.allocated.size
    };
  }

  getUsage() {
    return this.usedSize / this.totalSize;
  }

  async grow() {
    if (!this.config.growable) {
      throw new Error('Pool is not growable');
    }
    
    const currentSize = this.totalSize;
    const maxSize = currentSize * this.config.maxGrowth;
    
    if (this.totalSize >= maxSize) {
      throw new Error('Maximum pool size reached');
    }
    
    this.totalSize = Math.min(this.totalSize * 1.5, maxSize);
    console.log(`Pool ${this.config.name} grown to ${this.totalSize}`);
  }
}
```

## 3. 볼트 구조 설계

### 3.1 계층적 구조 설계
```javascript
// 볼트 구조 설계자
class VaultStructureDesigner {
  constructor() {
    this.patterns = {
      'hierarchical': new HierarchicalPattern(),
      'flat': new FlatPattern(),
      'hybrid': new HybridPattern(),
      'domain-driven': new DomainDrivenPattern(),
      'zettelkasten': new ZettelkastenPattern()
    };
    
    this.analyzer = new StructureAnalyzer();
  }

  // 최적 구조 추천
  async recommendStructure(vaultInfo) {
    const analysis = await this.analyzer.analyze(vaultInfo);
    
    const scores = {};
    
    for (const [name, pattern] of Object.entries(this.patterns)) {
      scores[name] = pattern.evaluate(analysis);
    }
    
    // 점수별 정렬
    const recommendations = Object.entries(scores)
      .sort((a, b) => b[1] - a[1])
      .map(([pattern, score]) => ({
        pattern,
        score,
        structure: this.patterns[pattern].generate(analysis)
      }));
    
    return recommendations;
  }

  // 구조 구현
  async implementStructure(vaultPath, structure) {
    console.log(`Implementing ${structure.pattern} structure...`);
    
    const pattern = this.patterns[structure.pattern];
    const plan = await pattern.createImplementationPlan(vaultPath, structure);
    
    // 백업
    await this.backupCurrentStructure(vaultPath);
    
    // 단계별 실행
    for (const step of plan.steps) {
      await this.executeStep(step);
      
      // 검증
      if (!await this.validateStep(step)) {
        throw new Error(`Step validation failed: ${step.name}`);
      }
    }
    
    // 최종 검증
    await this.validateStructure(vaultPath, structure);
    
    console.log('Structure implementation complete');
  }

  // 단계 실행
  async executeStep(step) {
    switch (step.type) {
      case 'create-folder':
        await this.createFolder(step.path);
        break;
        
      case 'move-files':
        await this.moveFiles(step.files, step.destination);
        break;
        
      case 'rename':
        await this.rename(step.from, step.to);
        break;
        
      case 'merge-folders':
        await this.mergeFolders(step.folders, step.destination);
        break;
        
      case 'split-folder':
        await this.splitFolder(step.folder, step.strategy);
        break;
    }
  }
}

// 계층적 패턴
class HierarchicalPattern {
  evaluate(analysis) {
    let score = 0;
    
    // 노트 수가 많을수록 유리
    if (analysis.totalNotes > 10000) score += 30;
    else if (analysis.totalNotes > 1000) score += 20;
    
    // 명확한 카테고리가 있을 때 유리
    if (analysis.categories.length > 5) score += 25;
    
    // 팀 사용 시 유리
    if (analysis.teamSize > 1) score += 20;
    
    // 복잡한 프로젝트에 유리
    if (analysis.projectComplexity > 7) score += 15;
    
    return score;
  }

  generate(analysis) {
    return {
      pattern: 'hierarchical',
      structure: {
        maxDepth: 5,
        maxItemsPerFolder: 200,
        levels: [
          { name: 'Areas', type: 'category' },
          { name: 'Projects', type: 'project' },
          { name: 'Topics', type: 'topic' },
          { name: 'Subtopics', type: 'subtopic' },
          { name: 'Notes', type: 'note' }
        ],
        rules: {
          naming: 'descriptive',
          sorting: 'alphabetical',
          archiving: 'yearly'
        }
      }
    };
  }

  async createImplementationPlan(vaultPath, structure) {
    const plan = {
      steps: [],
      estimatedTime: 0
    };

    // 1. 최상위 폴더 생성
    structure.structure.levels.forEach((level, index) => {
      if (index === 0) {
        plan.steps.push({
          type: 'create-folder',
          path: `${vaultPath}/${level.name}`,
          name: `Create ${level.name} folders`
        });
      }
    });

    // 2. 기존 파일 분류
    plan.steps.push({
      type: 'classify-files',
      strategy: 'content-based',
      name: 'Classify existing files'
    });

    // 3. 파일 이동
    plan.steps.push({
      type: 'move-files',
      batch: true,
      name: 'Move files to new structure'
    });

    // 4. 인덱스 생성
    plan.steps.push({
      type: 'create-index',
      path: `${vaultPath}/Index.md`,
      name: 'Create master index'
    });

    return plan;
  }
}

// 플랫 패턴
class FlatPattern {
  evaluate(analysis) {
    let score = 0;
    
    // 노트 수가 적을 때 유리
    if (analysis.totalNotes < 1000) score += 30;
    
    // 빠른 접근이 중요할 때
    if (analysis.accessPattern === 'random') score += 25;
    
    // 태그 기반 조직을 선호할 때
    if (analysis.tagUsage > 0.8) score += 30;
    
    // 개인 사용에 유리
    if (analysis.teamSize === 1) score += 15;
    
    return score;
  }

  generate(analysis) {
    return {
      pattern: 'flat',
      structure: {
        folders: [
          'Daily',
          'Projects',
          'Archive',
          'Templates',
          'Attachments'
        ],
        organization: 'tag-based',
        naming: 'timestamp-prefix',
        rules: {
          fileNaming: 'YYYY-MM-DD-title',
          tagPrefix: true,
          autoArchive: 90 // days
        }
      }
    };
  }
}

// 하이브리드 패턴
class HybridPattern {
  evaluate(analysis) {
    let score = 50; // 기본 점수
    
    // 중간 규모에 최적
    if (analysis.totalNotes >= 1000 && analysis.totalNotes <= 10000) {
      score += 20;
    }
    
    // 다양한 콘텐츠 타입
    if (analysis.contentTypes.length > 3) score += 15;
    
    // 혼합된 사용 패턴
    if (analysis.accessPattern === 'mixed') score += 15;
    
    return score;
  }

  generate(analysis) {
    return {
      pattern: 'hybrid',
      structure: {
        core: {
          hierarchical: ['Projects', 'Areas', 'Resources'],
          flat: ['Daily', 'Quick Notes', 'Inbox']
        },
        rules: {
          inboxProcessing: 'weekly',
          projectStructure: 'hierarchical',
          dailyStructure: 'flat',
          archiving: 'selective'
        },
        automation: {
          sorting: true,
          tagging: true,
          linking: true
        }
      }
    };
  }
}

// 도메인 주도 패턴
class DomainDrivenPattern {
  evaluate(analysis) {
    let score = 0;
    
    // 명확한 도메인이 있을 때
    if (analysis.domains.length > 0) score += 40;
    
    // 전문 분야에 유리
    if (analysis.specialization > 0.7) score += 30;
    
    // 대규모 지식베이스
    if (analysis.totalNotes > 5000) score += 20;
    
    // 팀 협업
    if (analysis.teamSize > 5) score += 10;
    
    return score;
  }

  generate(analysis) {
    const domains = analysis.domains || ['Domain1', 'Domain2'];
    
    return {
      pattern: 'domain-driven',
      structure: {
        domains: domains.map(domain => ({
          name: domain,
          subfolders: [
            'Concepts',
            'Entities',
            'Processes',
            'References',
            'Examples'
          ]
        })),
        shared: [
          'Cross-Domain',
          'Integration',
          'Standards',
          'Glossary'
        ],
        rules: {
          boundedContext: true,
          ubiquitousLanguage: true,
          aggregateRoots: true
        }
      }
    };
  }
}
```

### 3.2 자동 구조 최적화
```javascript
// 구조 최적화 엔진
class StructureOptimizationEngine {
  constructor() {
    this.optimizer = new StructureOptimizer();
    this.reorganizer = new VaultReorganizer();
    this.validator = new StructureValidator();
  }

  // 자동 최적화 실행
  async optimizeStructure(vaultPath, options = {}) {
    console.log('Starting structure optimization...');
    
    // 1. 현재 구조 분석
    const currentStructure = await this.analyzeCurrentStructure(vaultPath);
    
    // 2. 문제점 식별
    const issues = await this.identifyIssues(currentStructure);
    
    if (issues.length === 0) {
      console.log('No structural issues found');
      return { optimized: false, reason: 'Already optimal' };
    }
    
    // 3. 최적화 계획 생성
    const plan = await this.optimizer.createOptimizationPlan(
      currentStructure,
      issues,
      options
    );
    
    // 4. 사용자 승인 (옵션)
    if (!options.autoApprove) {
      const approved = await this.requestApproval(plan);
      if (!approved) {
        return { optimized: false, reason: 'User cancelled' };
      }
    }
    
    // 5. 백업
    const backupPath = await this.createBackup(vaultPath);
    
    try {
      // 6. 최적화 실행
      await this.executeOptimization(plan);
      
      // 7. 검증
      const valid = await this.validator.validate(vaultPath);
      
      if (!valid) {
        throw new Error('Validation failed after optimization');
      }
      
      // 8. 인덱스 재구축
      await this.rebuildIndices(vaultPath);
      
      console.log('Structure optimization complete');
      
      return {
        optimized: true,
        changes: plan.changes,
        improvements: plan.estimatedImprovements,
        backupPath
      };
      
    } catch (error) {
      // 롤백
      console.error('Optimization failed, rolling back...', error);
      await this.rollback(vaultPath, backupPath);
      
      throw error;
    }
  }

  // 현재 구조 분석
  async analyzeCurrentStructure(vaultPath) {
    const structure = {
      path: vaultPath,
      metrics: {},
      patterns: {},
      issues: []
    };
    
    // 깊이 분석
    structure.metrics.depth = await this.analyzer.measureDepth(vaultPath);
    
    // 밀도 분석
    structure.metrics.density = await this.analyzer.measureDensity(vaultPath);
    
    // 균형 분석
    structure.metrics.balance = await this.analyzer.measureBalance(vaultPath);
    
    // 네이밍 패턴
    structure.patterns.naming = await this.analyzer.analyzeNamingPatterns(vaultPath);
    
    // 구조 패턴
    structure.patterns.structural = await this.analyzer.analyzeStructuralPatterns(vaultPath);
    
    return structure;
  }

  // 문제점 식별
  async identifyIssues(structure) {
    const issues = [];
    
    // 깊이 문제
    if (structure.metrics.depth.max > 7) {
      issues.push({
        type: 'excessive-depth',
        severity: 'high',
        location: structure.metrics.depth.deepestPath,
        impact: 'Navigation difficulty'
      });
    }
    
    // 밀도 문제
    const densityIssues = structure.metrics.density.folders
      .filter(f => f.fileCount > 500);
    
    densityIssues.forEach(folder => {
      issues.push({
        type: 'overcrowded-folder',
        severity: 'high',
        location: folder.path,
        fileCount: folder.fileCount,
        impact: 'Performance degradation'
      });
    });
    
    // 균형 문제
    if (structure.metrics.balance.coefficient < 0.5) {
      issues.push({
        type: 'unbalanced-structure',
        severity: 'medium',
        impact: 'Inefficient organization'
      });
    }
    
    // 네이밍 문제
    if (structure.patterns.naming.consistency < 0.7) {
      issues.push({
        type: 'inconsistent-naming',
        severity: 'low',
        impact: 'Reduced searchability'
      });
    }
    
    // 고아 파일
    const orphans = await this.findOrphanFiles(structure);
    if (orphans.length > 0) {
      issues.push({
        type: 'orphan-files',
        severity: 'medium',
        files: orphans,
        impact: 'Lost content'
      });
    }
    
    return issues;
  }

  // 최적화 실행
  async executeOptimization(plan) {
    const executor = new OptimizationExecutor();
    
    for (const change of plan.changes) {
      console.log(`Executing: ${change.description}`);
      
      await executor.execute(change);
      
      // 진행률 업데이트
      const progress = ((plan.changes.indexOf(change) + 1) / plan.changes.length * 100).toFixed(1);
      console.log(`Progress: ${progress}%`);
    }
  }
}

// 구조 최적화기
class StructureOptimizer {
  // 최적화 계획 생성
  async createOptimizationPlan(structure, issues, options) {
    const plan = {
      changes: [],
      estimatedImprovements: {},
      estimatedTime: 0
    };
    
    // 이슈별 해결책
    for (const issue of issues) {
      const solutions = await this.generateSolutions(issue, structure);
      const bestSolution = this.selectBestSolution(solutions, options);
      
      if (bestSolution) {
        plan.changes.push(...bestSolution.changes);
        
        // 개선 효과 추정
        Object.entries(bestSolution.improvements).forEach(([key, value]) => {
          plan.estimatedImprovements[key] = 
            (plan.estimatedImprovements[key] || 0) + value;
        });
      }
    }
    
    // 변경 사항 최적화 (중복 제거, 순서 조정)
    plan.changes = this.optimizeChanges(plan.changes);
    
    // 시간 추정
    plan.estimatedTime = this.estimateExecutionTime(plan.changes);
    
    return plan;
  }

  // 해결책 생성
  async generateSolutions(issue, structure) {
    const solutions = [];
    
    switch (issue.type) {
      case 'overcrowded-folder':
        solutions.push(
          this.generateShardingSolution(issue),
          this.generateCategorizationSolution(issue),
          this.generateArchivingSolution(issue)
        );
        break;
        
      case 'excessive-depth':
        solutions.push(
          this.generateFlatteningSolution(issue),
          this.generateRebalancingSolution(issue)
        );
        break;
        
      case 'unbalanced-structure':
        solutions.push(
          this.generateRedistributionSolution(issue, structure)
        );
        break;
        
      case 'inconsistent-naming':
        solutions.push(
          this.generateRenamingSolution(issue, structure)
        );
        break;
        
      case 'orphan-files':
        solutions.push(
          this.generateOrphanResolution(issue)
        );
        break;
    }
    
    return solutions;
  }

  // 샤딩 솔루션
  generateShardingSolution(issue) {
    return {
      type: 'sharding',
      changes: [
        {
          type: 'create-shards',
          folder: issue.location,
          strategy: 'alphabetical',
          shardCount: Math.ceil(issue.fileCount / 200),
          description: `Shard folder ${issue.location} into alphabetical subfolders`
        },
        {
          type: 'redistribute-files',
          source: issue.location,
          strategy: 'alphabetical',
          description: 'Redistribute files to shards'
        }
      ],
      improvements: {
        performance: 40,
        navigation: 30
      },
      risk: 'low'
    };
  }

  // 카테고리화 솔루션
  generateCategorizationSolution(issue) {
    return {
      type: 'categorization',
      changes: [
        {
          type: 'analyze-content',
          folder: issue.location,
          description: 'Analyze content for categorization'
        },
        {
          type: 'create-categories',
          folder: issue.location,
          description: 'Create category folders'
        },
        {
          type: 'move-by-category',
          folder: issue.location,
          description: 'Move files to category folders'
        }
      ],
      improvements: {
        organization: 50,
        searchability: 30
      },
      risk: 'medium'
    };
  }

  // 변경 사항 최적화
  optimizeChanges(changes) {
    // 의존성 그래프 생성
    const graph = this.buildDependencyGraph(changes);
    
    // 토폴로지 정렬
    const sorted = this.topologicalSort(graph);
    
    // 병렬 실행 가능한 작업 식별
    const optimized = this.identifyParallelizable(sorted);
    
    return optimized;
  }
}

// 볼트 재구성기
class VaultReorganizer {
  constructor() {
    this.fileOperations = new FileOperations();
    this.metadataManager = new MetadataManager();
  }

  // 폴더 분할
  async splitFolder(folderPath, strategy) {
    const files = await this.fileOperations.listFiles(folderPath);
    const groups = this.groupFiles(files, strategy);
    
    // 하위 폴더 생성
    for (const [groupName, groupFiles] of groups) {
      const subfolderPath = `${folderPath}/${groupName}`;
      await this.fileOperations.createFolder(subfolderPath);
      
      // 파일 이동
      for (const file of groupFiles) {
        await this.moveFileWithMetadata(
          file.path,
          `${subfolderPath}/${file.name}`
        );
      }
    }
  }

  // 파일 그룹화
  groupFiles(files, strategy) {
    const groups = new Map();
    
    switch (strategy) {
      case 'alphabetical':
        files.forEach(file => {
          const firstChar = file.name[0].toUpperCase();
          const groupKey = /[A-Z]/.test(firstChar) ? firstChar : '#';
          
          if (!groups.has(groupKey)) {
            groups.set(groupKey, []);
          }
          groups.get(groupKey).push(file);
        });
        break;
        
      case 'date':
        files.forEach(file => {
          const date = new Date(file.created);
          const groupKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
          
          if (!groups.has(groupKey)) {
            groups.set(groupKey, []);
          }
          groups.get(groupKey).push(file);
        });
        break;
        
      case 'type':
        files.forEach(file => {
          const groupKey = file.extension || 'no-extension';
          
          if (!groups.has(groupKey)) {
            groups.set(groupKey, []);
          }
          groups.get(groupKey).push(file);
        });
        break;
        
      case 'size':
        files.forEach(file => {
          const groupKey = this.getSizeGroup(file.size);
          
          if (!groups.has(groupKey)) {
            groups.set(groupKey, []);
          }
          groups.get(groupKey).push(file);
        });
        break;
    }
    
    return groups;
  }

  // 메타데이터 보존하며 파일 이동
  async moveFileWithMetadata(sourcePath, targetPath) {
    // 메타데이터 백업
    const metadata = await this.metadataManager.getMetadata(sourcePath);
    
    // 파일 이동
    await this.fileOperations.moveFile(sourcePath, targetPath);
    
    // 메타데이터 복원
    await this.metadataManager.setMetadata(targetPath, metadata);
    
    // 링크 업데이트
    await this.updateLinks(sourcePath, targetPath);
  }

  // 링크 업데이트
  async updateLinks(oldPath, newPath) {
    const affectedFiles = await this.findFilesLinkingTo(oldPath);
    
    for (const file of affectedFiles) {
      const content = await this.fileOperations.readFile(file);
      const updated = content.replace(
        new RegExp(`\\[\\[${oldPath}\\]\\]`, 'g'),
        `[[${newPath}]]`
      );
      
      if (content !== updated) {
        await this.fileOperations.writeFile(file, updated);
      }
    }
  }

  getSizeGroup(size) {
    if (size < 10 * 1024) return 'tiny';
    if (size < 100 * 1024) return 'small';
    if (size < 1024 * 1024) return 'medium';
    if (size < 10 * 1024 * 1024) return 'large';
    return 'huge';
  }
}
```

## 4. 백업과 복구

### 4.1 백업 전략
```javascript
// 백업 관리자
class BackupManager {
  constructor() {
    this.strategies = {
      'incremental': new IncrementalBackupStrategy(),
      'differential': new DifferentialBackupStrategy(),
      'full': new FullBackupStrategy(),
      'snapshot': new SnapshotBackupStrategy()
    };
    
    this.scheduler = new BackupScheduler();
    this.storage = new BackupStorage();
    this.encryption = new BackupEncryption();
  }

  // 백업 정책 설정
  async setBackupPolicy(policy) {
    this.policy = {
      strategy: policy.strategy || 'incremental',
      schedule: policy.schedule || 'daily',
      retention: policy.retention || 30, // days
      encryption: policy.encryption !== false,
      compression: policy.compression !== false,
      verification: policy.verification !== false,
      destinations: policy.destinations || ['local'],
      maxSize: policy.maxSize || 10 * 1024 * 1024 * 1024 // 10GB
    };
    
    // 스케줄 설정
    await this.scheduler.schedule(this.policy);
    
    console.log('Backup policy configured:', this.policy);
  }

  // 백업 실행
  async backup(vaultPath, options = {}) {
    const backupId = crypto.randomUUID();
    const timestamp = new Date();
    
    console.log(`Starting backup ${backupId}...`);
    
    try {
      // 1. 백업 전략 선택
      const strategy = this.strategies[options.strategy || this.policy.strategy];
      
      // 2. 백업 데이터 수집
      const backupData = await strategy.collect(vaultPath, this.getLastBackup());
      
      // 3. 압축
      if (this.policy.compression) {
        backupData.compressed = await this.compress(backupData.files);
      }
      
      // 4. 암호화
      if (this.policy.encryption) {
        backupData.encrypted = await this.encryption.encrypt(
          backupData.compressed || backupData.files
        );
      }
      
      // 5. 저장
      const backup = {
        id: backupId,
        timestamp,
        type: strategy.type,
        vault: vaultPath,
        size: backupData.size,
        fileCount: backupData.fileCount,
        checksum: await this.calculateChecksum(backupData),
        metadata: {
          ...backupData.metadata,
          policy: this.policy
        }
      };
      
      // 여러 대상에 저장
      for (const destination of this.policy.destinations) {
        await this.storage.save(destination, backup, backupData);
      }
      
      // 6. 검증
      if (this.policy.verification) {
        await this.verifyBackup(backup);
      }
      
      // 7. 정리
      await this.cleanupOldBackups();
      
      console.log(`Backup ${backupId} completed successfully`);
      
      return backup;
      
    } catch (error) {
      console.error(`Backup failed: ${error.message}`);
      
      // 실패 알림
      await this.notifyBackupFailure(backupId, error);
      
      throw error;
    }
  }

  // 복구
  async restore(backupId, options = {}) {
    console.log(`Starting restore from backup ${backupId}...`);
    
    try {
      // 1. 백업 찾기
      const backup = await this.storage.find(backupId);
      if (!backup) {
        throw new Error(`Backup not found: ${backupId}`);
      }
      
      // 2. 백업 데이터 로드
      const backupData = await this.storage.load(backup);
      
      // 3. 복호화
      if (backup.metadata.policy.encryption) {
        backupData.decrypted = await this.encryption.decrypt(backupData.encrypted);
      }
      
      // 4. 압축 해제
      if (backup.metadata.policy.compression) {
        backupData.decompressed = await this.decompress(
          backupData.decrypted || backupData.compressed
        );
      }
      
      // 5. 검증
      const valid = await this.verifyChecksum(
        backupData.decompressed || backupData.files,
        backup.checksum
      );
      
      if (!valid) {
        throw new Error('Backup integrity check failed');
      }
      
      // 6. 복구 전략 선택
      const strategy = this.strategies[backup.type];
      
      // 7. 복구 실행
      const targetPath = options.targetPath || backup.vault;
      
      if (options.mode === 'overwrite') {
        // 기존 데이터 백업
        await this.backup(targetPath, { strategy: 'snapshot' });
      }
      
      await strategy.restore(backupData, targetPath, options);
      
      // 8. 복구 검증
      await this.verifyRestore(targetPath, backup);
      
      console.log(`Restore completed successfully`);
      
      return {
        backupId,
        restoredFiles: backupData.fileCount,
        targetPath
      };
      
    } catch (error) {
      console.error(`Restore failed: ${error.message}`);
      throw error;
    }
  }

  // 이전 백업 정보
  getLastBackup() {
    return this.storage.getLastBackup(this.policy.strategy);
  }

  // 오래된 백업 정리
  async cleanupOldBackups() {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - this.policy.retention);
    
    const oldBackups = await this.storage.findOlderThan(cutoffDate);
    
    for (const backup of oldBackups) {
      // 보존 정책 확인
      if (!this.shouldRetain(backup)) {
        await this.storage.delete(backup.id);
        console.log(`Deleted old backup: ${backup.id}`);
      }
    }
  }

  // 보존 여부 결정
  shouldRetain(backup) {
    // 월간 백업은 1년간 보존
    if (backup.timestamp.getDate() === 1) {
      const oneYearAgo = new Date();
      oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
      return backup.timestamp > oneYearAgo;
    }
    
    // 주간 백업은 3개월간 보존
    if (backup.timestamp.getDay() === 0) {
      const threeMonthsAgo = new Date();
      threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
      return backup.timestamp > threeMonthsAgo;
    }
    
    // 일반 정책 적용
    return false;
  }

  // 백업 검증
  async verifyBackup(backup) {
    console.log('Verifying backup integrity...');
    
    // 샘플 복구 테스트
    const tempPath = `/tmp/backup-verify-${backup.id}`;
    
    try {
      await this.restore(backup.id, {
        targetPath: tempPath,
        mode: 'test'
      });
      
      // 정리
      await this.storage.cleanup(tempPath);
      
      console.log('Backup verification passed');
      
    } catch (error) {
      console.error('Backup verification failed:', error);
      throw error;
    }
  }
}

// 증분 백업 전략
class IncrementalBackupStrategy {
  constructor() {
    this.type = 'incremental';
  }

  async collect(vaultPath, lastBackup) {
    const changes = await this.detectChanges(vaultPath, lastBackup);
    
    return {
      type: this.type,
      files: changes.files,
      deleted: changes.deleted,
      size: changes.totalSize,
      fileCount: changes.files.length,
      metadata: {
        baseBackup: lastBackup?.id,
        changesOnly: true
      }
    };
  }

  async detectChanges(vaultPath, lastBackup) {
    if (!lastBackup) {
      // 첫 백업은 전체 백업
      return await this.collectAll(vaultPath);
    }
    
    const changes = {
      files: [],
      deleted: [],
      totalSize: 0
    };
    
    const lastBackupDate = new Date(lastBackup.timestamp);
    const files = await this.getAllFiles(vaultPath);
    
    for (const file of files) {
      const stats = await this.getFileStats(file);
      
      if (stats.mtime > lastBackupDate) {
        changes.files.push({
          path: file,
          size: stats.size,
          mtime: stats.mtime,
          content: await this.readFile(file)
        });
        
        changes.totalSize += stats.size;
      }
    }
    
    // 삭제된 파일 감지
    if (lastBackup.fileList) {
      const currentFiles = new Set(files);
      
      lastBackup.fileList.forEach(file => {
        if (!currentFiles.has(file)) {
          changes.deleted.push(file);
        }
      });
    }
    
    return changes;
  }

  async restore(backupData, targetPath, options) {
    // 기본 백업부터 순차적으로 복구
    if (backupData.metadata.baseBackup) {
      // 재귀적으로 이전 백업 복구
      await this.restoreBase(backupData.metadata.baseBackup, targetPath);
    }
    
    // 현재 변경사항 적용
    for (const file of backupData.files) {
      await this.restoreFile(file, targetPath);
    }
    
    // 삭제된 파일 처리
    if (backupData.deleted && options.mode !== 'merge') {
      for (const path of backupData.deleted) {
        await this.deleteFile(path, targetPath);
      }
    }
  }
}

// 스냅샷 백업 전략
class SnapshotBackupStrategy {
  constructor() {
    this.type = 'snapshot';
  }

  async collect(vaultPath) {
    console.log('Creating vault snapshot...');
    
    const snapshot = {
      type: this.type,
      timestamp: new Date(),
      files: new Map(),
      structure: {},
      metadata: {
        complete: true,
        compressed: true
      }
    };
    
    // 전체 구조 캡처
    snapshot.structure = await this.captureStructure(vaultPath);
    
    // 모든 파일 수집
    const files = await this.getAllFiles(vaultPath);
    
    for (const file of files) {
      const content = await this.readFile(file);
      const compressed = await this.compressFile(content);
      
      snapshot.files.set(file, {
        content: compressed,
        stats: await this.getFileStats(file),
        checksum: this.calculateChecksum(content)
      });
    }
    
    return {
      ...snapshot,
      size: this.calculateTotalSize(snapshot.files),
      fileCount: snapshot.files.size
    };
  }

  async restore(snapshotData, targetPath, options) {
    // 전체 구조 복구
    await this.restoreStructure(snapshotData.structure, targetPath);
    
    // 모든 파일 복구
    for (const [path, fileData] of snapshotData.files) {
      const content = await this.decompressFile(fileData.content);
      
      // 체크섬 검증
      const checksum = this.calculateChecksum(content);
      if (checksum !== fileData.checksum) {
        throw new Error(`Checksum mismatch for file: ${path}`);
      }
      
      await this.writeFile(path, content, targetPath);
      
      // 메타데이터 복구
      await this.restoreFileStats(path, fileData.stats, targetPath);
    }
  }

  async captureStructure(vaultPath) {
    const structure = {
      folders: [],
      links: new Map(),
      tags: new Map(),
      metadata: {}
    };
    
    // 폴더 구조
    structure.folders = await this.getAllFolders(vaultPath);
    
    // 링크 관계
    const files = await this.getAllFiles(vaultPath);
    for (const file of files) {
      const links = await this.extractLinks(file);
      if (links.length > 0) {
        structure.links.set(file, links);
      }
    }
    
    // 태그 인덱스
    for (const file of files) {
      const tags = await this.extractTags(file);
      tags.forEach(tag => {
        if (!structure.tags.has(tag)) {
          structure.tags.set(tag, []);
        }
        structure.tags.get(tag).push(file);
      });
    }
    
    return structure;
  }
}

// 백업 스케줄러
class BackupScheduler {
  constructor() {
    this.jobs = new Map();
    this.cron = require('node-cron');
  }

  async schedule(policy) {
    // 기존 스케줄 취소
    if (this.jobs.has('backup')) {
      this.jobs.get('backup').stop();
    }
    
    // 크론 표현식 생성
    const cronExpression = this.getCronExpression(policy.schedule);
    
    // 스케줄 등록
    const job = this.cron.schedule(cronExpression, async () => {
      console.log('Scheduled backup starting...');
      
      try {
        await this.executeBackup(policy);
      } catch (error) {
        console.error('Scheduled backup failed:', error);
        await this.notifyFailure(error);
      }
    });
    
    this.jobs.set('backup', job);
    job.start();
    
    console.log(`Backup scheduled: ${policy.schedule}`);
  }

  getCronExpression(schedule) {
    const expressions = {
      'hourly': '0 * * * *',
      'daily': '0 2 * * *',      // 2 AM
      'weekly': '0 2 * * 0',     // Sunday 2 AM
      'monthly': '0 2 1 * *'     // 1st day of month 2 AM
    };
    
    return expressions[schedule] || schedule;
  }
}
```

### 4.2 재해 복구
```javascript
// 재해 복구 시스템
class DisasterRecoverySystem {
  constructor() {
    this.backup = new BackupManager();
    this.replication = new ReplicationManager();
    this.failover = new FailoverManager();
    this.monitor = new HealthMonitor();
  }

  // 재해 복구 계획 수립
  async createDisasterRecoveryPlan(vaultConfig) {
    const plan = {
      id: crypto.randomUUID(),
      created: new Date(),
      vault: vaultConfig,
      objectives: {
        rpo: vaultConfig.rpo || 3600,    // Recovery Point Objective (seconds)
        rto: vaultConfig.rto || 14400,   // Recovery Time Objective (seconds)
        dataLoss: vaultConfig.maxDataLoss || 0.01 // 1%
      },
      strategies: [],
      procedures: [],
      testing: {
        frequency: 'monthly',
        lastTest: null,
        nextTest: null
      }
    };

    // 전략 선택
    if (plan.objectives.rpo < 300) { // 5분 미만
      plan.strategies.push({
        type: 'real-time-replication',
        priority: 1
      });
    }
    
    if (plan.objectives.rto < 3600) { // 1시간 미만
      plan.strategies.push({
        type: 'hot-standby',
        priority: 1
      });
    }
    
    // 백업 전략
    plan.strategies.push({
      type: 'multi-site-backup',
      sites: ['local', 'cloud-primary', 'cloud-secondary'],
      priority: 2
    });
    
    // 복구 절차 생성
    plan.procedures = await this.generateRecoveryProcedures(plan);
    
    // 테스트 일정
    plan.testing.nextTest = this.calculateNextTestDate();
    
    return plan;
  }

  // 복구 절차 생성
  async generateRecoveryProcedures(plan) {
    const procedures = [];
    
    // 1. 초기 평가
    procedures.push({
      step: 1,
      name: 'Initial Assessment',
      actions: [
        'Identify failure type and scope',
        'Assess data loss extent',
        'Determine recovery strategy'
      ],
      estimatedTime: 300, // 5 minutes
      responsible: 'DR Team Lead'
    });
    
    // 2. 알림 및 에스컬레이션
    procedures.push({
      step: 2,
      name: 'Notification',
      actions: [
        'Notify stakeholders',
        'Activate DR team',
        'Update status page'
      ],
      estimatedTime: 600,
      responsible: 'Communications Lead'
    });
    
    // 3. 복구 실행
    procedures.push({
      step: 3,
      name: 'Recovery Execution',
      actions: this.getRecoveryActions(plan),
      estimatedTime: plan.objectives.rto * 0.7,
      responsible: 'Technical Lead'
    });
    
    // 4. 검증
    procedures.push({
      step: 4,
      name: 'Validation',
      actions: [
        'Verify data integrity',
        'Test critical functions',
        'Confirm user access'
      ],
      estimatedTime: 1800,
      responsible: 'QA Lead'
    });
    
    // 5. 전환
    procedures.push({
      step: 5,
      name: 'Cutover',
      actions: [
        'Update DNS/routing',
        'Enable user access',
        'Monitor performance'
      ],
      estimatedTime: 900,
      responsible: 'Operations Lead'
    });
    
    return procedures;
  }

  // 재해 감지 및 대응
  async detectAndRespond() {
    this.monitor.on('failure-detected', async (event) => {
      console.error('Disaster detected:', event);
      
      // 자동 대응 시작
      const response = await this.initiateDisasterResponse(event);
      
      // 알림
      await this.notifyStakeholders(event, response);
      
      // 복구 시작
      if (response.autoRecover) {
        await this.executeRecovery(response.plan);
      }
    });
  }

  // 재해 대응 시작
  async initiateDisasterResponse(event) {
    const response = {
      id: crypto.randomUUID(),
      event,
      timestamp: new Date(),
      severity: this.assessSeverity(event),
      autoRecover: false,
      plan: null
    };
    
    // 심각도에 따른 대응
    switch (response.severity) {
      case 'critical':
        // 즉시 자동 복구
        response.autoRecover = true;
        response.plan = await this.selectRecoveryPlan(event);
        break;
        
      case 'major':
        // 승인 후 복구
        response.plan = await this.selectRecoveryPlan(event);
        response.requiresApproval = true;
        break;
        
      case 'minor':
        // 모니터링만
        response.monitorOnly = true;
        break;
    }
    
    return response;
  }

  // 복구 실행
  async executeRecovery(plan) {
    console.log('Executing disaster recovery plan...');
    
    const execution = {
      planId: plan.id,
      startTime: new Date(),
      steps: [],
      status: 'in-progress'
    };
    
    try {
      for (const procedure of plan.procedures) {
        console.log(`Executing: ${procedure.name}`);
        
        const stepResult = await this.executeProcedure(procedure);
        execution.steps.push(stepResult);
        
        if (!stepResult.success) {
          throw new Error(`Procedure failed: ${procedure.name}`);
        }
      }
      
      execution.status = 'completed';
      execution.endTime = new Date();
      execution.duration = execution.endTime - execution.startTime;
      
      console.log('Disaster recovery completed successfully');
      
    } catch (error) {
      execution.status = 'failed';
      execution.error = error.message;
      
      console.error('Disaster recovery failed:', error);
      
      // 에스컬레이션
      await this.escalate(execution);
    }
    
    return execution;
  }

  // 재해 복구 테스트
  async testDisasterRecovery(planId) {
    console.log('Starting disaster recovery test...');
    
    const plan = await this.getRecoveryPlan(planId);
    const testEnvironment = await this.createTestEnvironment();
    
    const test = {
      id: crypto.randomUUID(),
      planId,
      timestamp: new Date(),
      environment: testEnvironment,
      results: []
    };
    
    try {
      // 1. 테스트 환경 준비
      await this.prepareTestEnvironment(testEnvironment);
      
      // 2. 재해 시뮬레이션
      await this.simulateDisaster(testEnvironment, plan.scenarios[0]);
      
      // 3. 복구 실행
      const recovery = await this.executeRecovery(plan);
      
      // 4. 검증
      const validation = await this.validateRecovery(testEnvironment);
      
      test.results = {
        recovery,
        validation,
        success: validation.passed,
        rpoAchieved: validation.dataLoss <= plan.objectives.dataLoss,
        rtoAchieved: recovery.duration <= plan.objectives.rto * 1000
      };
      
      // 5. 보고서 생성
      test.report = await this.generateTestReport(test);
      
    } finally {
      // 테스트 환경 정리
      await this.cleanupTestEnvironment(testEnvironment);
    }
    
    // 다음 테스트 일정
    plan.testing.lastTest = test.timestamp;
    plan.testing.nextTest = this.calculateNextTestDate();
    
    return test;
  }
}

// 복제 관리자
class ReplicationManager {
  constructor() {
    this.replicas = new Map();
    this.syncEngine = new SyncEngine();
  }

  // 복제 설정
  async setupReplication(source, targets, options = {}) {
    const replication = {
      id: crypto.randomUUID(),
      source,
      targets,
      mode: options.mode || 'async', // async, sync, semi-sync
      interval: options.interval || 5000, // 5초
      conflictResolution: options.conflictResolution || 'source-wins',
      encryption: options.encryption !== false,
      compression: options.compression !== false
    };
    
    // 각 타겟에 대한 복제 채널 설정
    for (const target of targets) {
      const channel = await this.createReplicationChannel(source, target, replication);
      this.replicas.set(`${source.id}-${target.id}`, channel);
    }
    
    // 복제 시작
    if (options.startImmediately !== false) {
      await this.startReplication(replication.id);
    }
    
    return replication;
  }

  // 복제 채널 생성
  async createReplicationChannel(source, target, config) {
    const channel = {
      id: crypto.randomUUID(),
      source,
      target,
      config,
      status: 'initialized',
      lastSync: null,
      lag: 0,
      errors: []
    };
    
    // 초기 동기화
    if (config.initialSync !== false) {
      await this.performInitialSync(channel);
    }
    
    // 변경 감지 설정
    if (config.mode === 'async') {
      this.setupChangeDetection(channel);
    }
    
    return channel;
  }

  // 실시간 복제
  async performRealtimeReplication(channel) {
    const changes = await this.detectChanges(channel.source, channel.lastSync);
    
    if (changes.length === 0) return;
    
    try {
      // 변경사항 전송
      const batch = this.createReplicationBatch(changes, channel.config);
      
      if (channel.config.encryption) {
        batch.encrypted = await this.encrypt(batch);
      }
      
      if (channel.config.compression) {
        batch.compressed = await this.compress(batch);
      }
      
      // 타겟에 적용
      await this.applyToTarget(channel.target, batch);
      
      // 상태 업데이트
      channel.lastSync = new Date();
      channel.lag = 0;
      
    } catch (error) {
      channel.errors.push({
        timestamp: new Date(),
        error: error.message
      });
      
      // 재시도 로직
      if (channel.errors.length < 3) {
        setTimeout(() => this.performRealtimeReplication(channel), 5000);
      } else {
        // 알림
        await this.notifyReplicationFailure(channel);
      }
    }
  }
}

// 페일오버 관리자
class FailoverManager {
  constructor() {
    this.primarySite = null;
    this.standbySites = [];
    this.failoverInProgress = false;
  }

  // 페일오버 설정
  async configureFailover(config) {
    this.primarySite = config.primary;
    this.standbySites = config.standby;
    this.strategy = config.strategy || 'automatic';
    this.healthCheckInterval = config.healthCheckInterval || 30000; // 30초
    
    // 건강 체크 시작
    this.startHealthChecks();
  }

  // 자동 페일오버
  async performAutomaticFailover() {
    if (this.failoverInProgress) {
      console.log('Failover already in progress');
      return;
    }
    
    this.failoverInProgress = true;
    
    try {
      // 1. 최적 스탠바이 선택
      const newPrimary = await this.selectBestStandby();
      
      if (!newPrimary) {
        throw new Error('No healthy standby available');
      }
      
      // 2. 데이터 동기화 확인
      await this.ensureDataConsistency(newPrimary);
      
      // 3. 프로모션
      await this.promoteStandby(newPrimary);
      
      // 4. 트래픽 전환
      await this.switchTraffic(this.primarySite, newPrimary);
      
      // 5. 이전 프라이머리 처리
      await this.demotePrimary(this.primarySite);
      
      // 6. 상태 업데이트
      this.primarySite = newPrimary;
      this.standbySites = this.standbySites.filter(s => s.id !== newPrimary.id);
      
      console.log(`Failover completed: ${newPrimary.id} is now primary`);
      
    } finally {
      this.failoverInProgress = false;
    }
  }

  // 최적 스탠바이 선택
  async selectBestStandby() {
    const candidates = [];
    
    for (const standby of this.standbySites) {
      const health = await this.checkHealth(standby);
      const lag = await this.checkReplicationLag(standby);
      
      if (health.status === 'healthy') {
        candidates.push({
          site: standby,
          score: this.calculateFailoverScore(health, lag)
        });
      }
    }
    
    // 점수순 정렬
    candidates.sort((a, b) => b.score - a.score);
    
    return candidates[0]?.site;
  }

  // 페일오버 점수 계산
  calculateFailoverScore(health, lag) {
    let score = 100;
    
    // 복제 지연 페널티
    score -= Math.min(lag.seconds, 50);
    
    // 리소스 사용률 페널티
    score -= (health.cpu + health.memory) / 2 * 0.3;
    
    // 지리적 위치 보너스
    if (health.region === this.primarySite.region) {
      score += 10;
    }
    
    return score;
  }
}
```

## 5. 대규모 팀 협업

### 5.1 협업 인프라
```javascript
// 대규모 팀 협업 시스템
class LargeScaleCollaborationSystem {
  constructor() {
    this.teams = new Map();
    this.permissions = new AdvancedPermissionSystem();
    this.conflicts = new ConflictResolutionEngine();
    this.workflows = new CollaborativeWorkflowEngine();
    this.communication = new CommunicationHub();
  }

  // 조직 구조 설정
  async setupOrganization(config) {
    const org = {
      id: crypto.randomUUID(),
      name: config.name,
      structure: config.structure || 'hierarchical',
      teams: new Map(),
      roles: new Map(),
      policies: config.policies || {}
    };

    // 역할 정의
    const defaultRoles = [
      { name: 'admin', level: 100, permissions: ['*'] },
      { name: 'team-lead', level: 80, permissions: ['read', 'write', 'review', 'merge'] },
      { name: 'senior-member', level: 60, permissions: ['read', 'write', 'review'] },
      { name: 'member', level: 40, permissions: ['read', 'write'] },
      { name: 'viewer', level: 20, permissions: ['read'] }
    ];

    defaultRoles.forEach(role => {
      org.roles.set(role.name, role);
    });

    // 팀 구조 생성
    await this.createTeamStructure(org, config.teams);

    return org;
  }

  // 팀 구조 생성
  async createTeamStructure(org, teamsConfig) {
    for (const teamConfig of teamsConfig) {
      const team = {
        id: crypto.randomUUID(),
        name: teamConfig.name,
        parent: teamConfig.parent,
        members: new Map(),
        vault: teamConfig.vault,
        permissions: new Map(),
        workflows: []
      };

      // 멤버 추가
      for (const member of teamConfig.members) {
        team.members.set(member.id, {
          ...member,
          joinedAt: new Date()
        });
      }

      // 권한 설정
      await this.permissions.setupTeamPermissions(team);

      // 워크플로우 설정
      team.workflows = await this.workflows.createTeamWorkflows(team);

      org.teams.set(team.id, team);
    }
  }

  // 협업 세션 관리
  async createCollaborationSession(projectId, participants) {
    const session = {
      id: crypto.randomUUID(),
      projectId,
      participants: new Map(),
      startTime: new Date(),
      activities: [],
      locks: new Map(),
      changes: []
    };

    // 참가자 설정
    for (const participant of participants) {
      session.participants.set(participant.id, {
        ...participant,
        status: 'active',
        lastActivity: new Date()
      });
    }

    // 실시간 협업 채널 설정
    const channel = await this.communication.createChannel(session);

    // 변경 추적 시작
    this.startChangeTracking(session);

    return { session, channel };
  }

  // 변경 추적
  startChangeTracking(session) {
    const tracker = new ChangeTracker();

    tracker.on('change', async (change) => {
      // 변경사항 기록
      session.changes.push({
        ...change,
        timestamp: new Date()
      });

      // 충돌 검사
      const conflicts = await this.conflicts.detect(change, session);

      if (conflicts.length > 0) {
        // 충돌 해결
        const resolution = await this.conflicts.resolve(conflicts, {
          strategy: 'collaborative',
          participants: Array.from(session.participants.values())
        });

        // 해결 결과 적용
        await this.applyResolution(resolution, session);
      }

      // 다른 참가자에게 브로드캐스트
      await this.broadcastChange(change, session);
    });
  }

  // 권한 기반 작업 분배
  async distributeWork(project, tasks) {
    const distribution = new Map();

    for (const task of tasks) {
      // 작업에 필요한 권한 확인
      const requiredPermissions = this.getRequiredPermissions(task);

      // 적합한 팀원 찾기
      const eligibleMembers = await this.findEligibleMembers(
        project,
        requiredPermissions
      );

      // 워크로드 밸런싱
      const assignee = this.selectOptimalAssignee(eligibleMembers, distribution);

      if (assignee) {
        distribution.set(task.id, {
          task,
          assignee,
          estimatedTime: this.estimateTaskTime(task, assignee)
        });
      }
    }

    return distribution;
  }

  // 대규모 리뷰 프로세스
  async setupReviewProcess(project) {
    const reviewConfig = {
      levels: [
        { name: 'peer', required: 2, permissions: ['review'] },
        { name: 'senior', required: 1, permissions: ['senior-review'] },
        { name: 'lead', required: 1, permissions: ['final-approval'] }
      ],
      rules: {
        autoAssign: true,
        timeLimit: 48 * 3600 * 1000, // 48시간
        escalation: true
      }
    };

    const reviewProcess = new ReviewProcess(reviewConfig);

    // 리뷰어 풀 설정
    const reviewerPool = await this.createReviewerPool(project);

    // 자동 할당 규칙
    reviewProcess.on('review-requested', async (request) => {
      const reviewers = await this.assignReviewers(
        request,
        reviewerPool,
        reviewConfig
      );

      // 알림 전송
      for (const reviewer of reviewers) {
        await this.communication.notify(reviewer, {
          type: 'review-request',
          request
        });
      }
    });

    return reviewProcess;
  }
}

// 고급 권한 시스템
class AdvancedPermissionSystem {
  constructor() {
    this.policies = new Map();
    this.inheritance = new PermissionInheritance();
    this.audit = new PermissionAudit();
  }

  // 계층적 권한 설정
  async setupHierarchicalPermissions(org) {
    const rootPolicy = {
      id: 'root',
      rules: [
        { resource: '*', permissions: ['read'], inherit: true },
        { resource: 'public/*', permissions: ['read', 'comment'], inherit: true }
      ]
    };

    // 팀별 정책
    for (const [teamId, team] of org.teams) {
      const teamPolicy = {
        id: `team-${teamId}`,
        parent: 'root',
        rules: [
          { resource: `${team.vault}/*`, permissions: ['read', 'write'], roles: ['member'] },
          { resource: `${team.vault}/drafts/*`, permissions: ['create', 'delete'], roles: ['member'] },
          { resource: `${team.vault}/published/*`, permissions: ['read'], roles: ['*'] }
        ]
      };

      this.policies.set(teamPolicy.id, teamPolicy);
    }
  }

  // 권한 확인
  async checkPermission(user, resource, action) {
    // 감사 로그
    this.audit.log({
      user,
      resource,
      action,
      timestamp: new Date()
    });

    // 직접 권한 확인
    const directPermission = await this.checkDirectPermission(user, resource, action);
    if (directPermission) return true;

    // 상속된 권한 확인
    const inheritedPermission = await this.inheritance.check(user, resource, action);
    if (inheritedPermission) return true;

    // 역할 기반 권한 확인
    const rolePermission = await this.checkRolePermission(user, resource, action);
    if (rolePermission) return true;

    return false;
  }

  // 동적 권한 부여
  async grantTemporaryPermission(user, resource, permissions, duration) {
    const grant = {
      id: crypto.randomUUID(),
      user,
      resource,
      permissions,
      grantedAt: new Date(),
      expiresAt: new Date(Date.now() + duration),
      active: true
    };

    // 임시 권한 저장
    await this.saveTemporaryGrant(grant);

    // 만료 스케줄링
    setTimeout(() => {
      this.revokeTemporaryPermission(grant.id);
    }, duration);

    return grant;
  }
}

// 충돌 해결 엔진
class ConflictResolutionEngine {
  constructor() {
    this.strategies = {
      'last-write-wins': new LastWriteWinsStrategy(),
      'collaborative': new CollaborativeStrategy(),
      'three-way-merge': new ThreeWayMergeStrategy(),
      'operational-transform': new OperationalTransformStrategy()
    };
  }

  // 충돌 감지
  async detect(change, session) {
    const conflicts = [];

    // 동시 편집 충돌
    const concurrentEdits = session.changes.filter(c =>
      c.file === change.file &&
      c.userId !== change.userId &&
      Math.abs(c.timestamp - change.timestamp) < 1000
    );

    if (concurrentEdits.length > 0) {
      conflicts.push({
        type: 'concurrent-edit',
        changes: [change, ...concurrentEdits]
      });
    }

    // 잠금 충돌
    const lock = session.locks.get(change.file);
    if (lock && lock.userId !== change.userId) {
      conflicts.push({
        type: 'lock-conflict',
        lock,
        change
      });
    }

    return conflicts;
  }

  // 충돌 해결
  async resolve(conflicts, options) {
    const resolutions = [];

    for (const conflict of conflicts) {
      const strategy = this.strategies[options.strategy || 'collaborative'];
      const resolution = await strategy.resolve(conflict, options);

      resolutions.push(resolution);
    }

    return resolutions;
  }
}

// 협업 전략
class CollaborativeStrategy {
  async resolve(conflict, options) {
    if (conflict.type === 'concurrent-edit') {
      // 변경사항 병합
      const merged = await this.mergeChanges(conflict.changes);

      // 참가자들에게 확인 요청
      if (options.participants) {
        const confirmations = await this.requestConfirmations(
          options.participants,
          merged
        );

        if (confirmations.every(c => c.approved)) {
          return {
            type: 'merge',
            result: merged,
            approved: true
          };
        }
      }

      // 수동 해결 필요
      return {
        type: 'manual',
        conflict,
        needsResolution: true
      };
    }

    return null;
  }

  async mergeChanges(changes) {
    // 변경사항을 시간순으로 정렬
    const sorted = changes.sort((a, b) => a.timestamp - b.timestamp);

    // 기본 내용
    let content = sorted[0].originalContent;

    // 각 변경사항 적용
    for (const change of sorted) {
      content = this.applyChange(content, change);
    }

    return {
      mergedContent: content,
      contributors: changes.map(c => c.userId),
      timestamp: new Date()
    };
  }

  applyChange(content, change) {
    // 간단한 줄 기반 병합
    const lines = content.split('\n');

    switch (change.type) {
      case 'insert':
        lines.splice(change.line, 0, change.text);
        break;

      case 'delete':
        lines.splice(change.line, change.count);
        break;

      case 'modify':
        lines[change.line] = change.text;
        break;
    }

    return lines.join('\n');
  }
}

// 커뮤니케이션 허브
class CommunicationHub {
  constructor() {
    this.channels = new Map();
    this.notifications = new NotificationSystem();
    this.presence = new PresenceTracker();
  }

  // 채널 생성
  async createChannel(session) {
    const channel = {
      id: session.id,
      type: 'collaboration',
      participants: new Map(),
      messages: [],
      events: new EventEmitter()
    };

    // WebSocket 연결 설정
    for (const [userId, participant] of session.participants) {
      const connection = await this.establishConnection(userId);

      channel.participants.set(userId, {
        ...participant,
        connection,
        status: 'online'
      });

      // 프레즌스 추적
      this.presence.track(userId, channel.id);
    }

    this.channels.set(channel.id, channel);

    return channel;
  }

  // 메시지 브로드캐스트
  async broadcast(channelId, message, excludeUser = null) {
    const channel = this.channels.get(channelId);
    if (!channel) return;

    for (const [userId, participant] of channel.participants) {
      if (userId === excludeUser) continue;

      if (participant.status === 'online' && participant.connection) {
        participant.connection.send(JSON.stringify(message));
      } else {
        // 오프라인 사용자에게는 알림 저장
        await this.notifications.queue(userId, message);
      }
    }

    // 메시지 기록
    channel.messages.push({
      ...message,
      timestamp: new Date()
    });
  }

  // 실시간 커서 공유
  async shareCursor(userId, channelId, cursorData) {
    await this.broadcast(channelId, {
      type: 'cursor-update',
      userId,
      cursor: cursorData
    }, userId);
  }

  // 실시간 선택 영역 공유
  async shareSelection(userId, channelId, selectionData) {
    await this.broadcast(channelId, {
      type: 'selection-update',
      userId,
      selection: selectionData
    }, userId);
  }
}

// 프레즌스 추적
class PresenceTracker {
  constructor() {
    this.presence = new Map();
    this.heartbeatInterval = 30000; // 30초
  }

  track(userId, channelId) {
    const key = `${userId}:${channelId}`;

    this.presence.set(key, {
      userId,
      channelId,
      status: 'online',
      lastSeen: new Date(),
      activity: 'idle'
    });

    // 하트비트 시작
    this.startHeartbeat(key);
  }

  startHeartbeat(key) {
    const interval = setInterval(() => {
      const presence = this.presence.get(key);

      if (!presence) {
        clearInterval(interval);
        return;
      }

      const now = new Date();
      const timeSinceLastSeen = now - presence.lastSeen;

      if (timeSinceLastSeen > this.heartbeatInterval * 2) {
        // 오프라인으로 표시
        presence.status = 'offline';
        this.broadcastPresenceUpdate(presence);
      }
    }, this.heartbeatInterval);
  }

  updateActivity(userId, channelId, activity) {
    const key = `${userId}:${channelId}`;
    const presence = this.presence.get(key);

    if (presence) {
      presence.activity = activity;
      presence.lastSeen = new Date();
      this.broadcastPresenceUpdate(presence);
    }
  }

  broadcastPresenceUpdate(presence) {
    // 채널의 다른 참가자들에게 프레즌스 업데이트 전송
    // 구현은 CommunicationHub와 연동
  }
}
```

## 6. 실습 프로젝트

### 6.1 엔터프라이즈 볼트 구축
```javascript
// 엔터프라이즈 볼트 구축 프로젝트
class EnterpriseVaultProject {
  constructor() {
    this.architecture = new ScalableVaultArchitecture();
    this.performance = new PerformanceOptimizer();
    this.backup = new BackupManager();
    this.collaboration = new LargeScaleCollaborationSystem();
  }

  // 프로젝트 실행
  async execute() {
    console.log('Starting Enterprise Vault Project...');

    // 1. 초기 설정
    const config = await this.gatherRequirements();

    // 2. 아키텍처 설계
    const architecture = await this.designArchitecture(config);

    // 3. 구현
    const implementation = await this.implement(architecture);

    // 4. 최적화
    const optimized = await this.optimize(implementation);

    // 5. 테스트
    const tested = await this.test(optimized);

    // 6. 배포
    const deployed = await this.deploy(tested);

    // 7. 모니터링
    await this.setupMonitoring(deployed);

    return deployed;
  }

  // 요구사항 수집
  async gatherRequirements() {
    return {
      scale: {
        currentNotes: 50000,
        expectedGrowth: '20% yearly',
        peakLoad: 1000, // concurrent users
      },
      teams: [
        { name: 'Research', size: 50 },
        { name: 'Engineering', size: 100 },
        { name: 'Documentation', size: 30 },
        { name: 'Management', size: 20 }
      ],
      performance: {
        searchLatency: 100, // ms
        indexingThroughput: 1000, // notes/second
        backupWindow: 4 * 3600 * 1000 // 4 hours
      },
      compliance: {
        dataRetention: 7 * 365 * 24 * 3600 * 1000, // 7 years
        encryption: 'AES-256',
        auditLog: true
      }
    };
  }

  // 아키텍처 설계
  async designArchitecture(config) {
    const design = {
      structure: {
        pattern: 'domain-driven',
        sharding: 'content-based',
        depth: 5,
        naming: 'semantic'
      },
      storage: {
        primary: 'high-performance-ssd',
        archive: 'cloud-storage',
        cache: 'distributed-memory'
      },
      indexing: {
        type: 'distributed',
        engines: ['full-text', 'semantic', 'metadata'],
        updateStrategy: 'incremental'
      },
      backup: {
        strategy: 'incremental-forever',
        destinations: ['local', 'cloud-primary', 'cloud-secondary'],
        schedule: 'continuous'
      },
      collaboration: {
        realtime: true,
        conflictResolution: 'operational-transform',
        permissions: 'role-based'
      }
    };

    return design;
  }

  // 구현
  async implement(architecture) {
    const steps = [
      'Setup infrastructure',
      'Create vault structure',
      'Import existing data',
      'Build indices',
      'Configure backup',
      'Setup collaboration',
      'Implement security'
    ];

    const results = {};

    for (const step of steps) {
      console.log(`Implementing: ${step}`);
      results[step] = await this.implementStep(step, architecture);
    }

    return results;
  }

  // 최적화
  async optimize(implementation) {
    // 성능 프로파일링
    const profile = await this.performance.profile(implementation);

    // 병목 지점 식별
    const bottlenecks = await this.performance.identifyBottlenecks(profile);

    // 최적화 적용
    const optimizations = [];

    for (const bottleneck of bottlenecks) {
      const optimization = await this.applyOptimization(bottleneck);
      optimizations.push(optimization);
    }

    return {
      ...implementation,
      optimizations,
      performanceGain: this.calculatePerformanceGain(optimizations)
    };
  }

  // 테스트
  async test(system) {
    const testSuite = {
      functional: [
        'Create/Read/Update/Delete operations',
        'Search functionality',
        'Collaboration features',
        'Backup and restore'
      ],
      performance: [
        'Load testing (1000 concurrent users)',
        'Stress testing (100k notes)',
        'Endurance testing (24 hours)'
      ],
      security: [
        'Access control',
        'Encryption verification',
        'Audit logging'
      ],
      disaster: [
        'Failover testing',
        'Data recovery',
        'Business continuity'
      ]
    };

    const results = {};

    for (const [category, tests] of Object.entries(testSuite)) {
      results[category] = await this.runTests(tests);
    }

    return results;
  }

  // 모니터링 설정
  async setupMonitoring(system) {
    const monitoring = {
      metrics: [
        'System performance',
        'User activity',
        'Storage usage',
        'Error rates'
      ],
      alerts: [
        { metric: 'cpu_usage', threshold: 80, action: 'scale' },
        { metric: 'storage_usage', threshold: 90, action: 'archive' },
        { metric: 'error_rate', threshold: 0.01, action: 'investigate' }
      ],
      dashboards: [
        'Executive overview',
        'Technical operations',
        'User analytics',
        'Security monitoring'
      ]
    };

    return await this.monitor.setup(monitoring);
  }
}

// 실행 예제
async function runEnterpriseVaultProject() {
  const project = new EnterpriseVaultProject();

  try {
    const result = await project.execute();

    console.log('Enterprise Vault Project completed successfully');
    console.log('Results:', result);

  } catch (error) {
    console.error('Project failed:', error);
  }
}
```

### 6.2 성능 벤치마크
```javascript
// 대규모 볼트 성능 벤치마크
class VaultPerformanceBenchmark {
  constructor() {
    this.scenarios = [];
    this.results = new Map();
  }

  // 벤치마크 실행
  async run(vaultPath) {
    console.log('Starting performance benchmark...');

    // 시나리오 정의
    this.defineScenarios();

    // 각 시나리오 실행
    for (const scenario of this.scenarios) {
      console.log(`Running scenario: ${scenario.name}`);

      const result = await this.runScenario(scenario, vaultPath);
      this.results.set(scenario.name, result);
    }

    // 보고서 생성
    const report = this.generateReport();

    return report;
  }

  // 시나리오 정의
  defineScenarios() {
    this.scenarios = [
      {
        name: 'Sequential Write',
        operations: 10000,
        concurrent: 1,
        action: 'write'
      },
      {
        name: 'Concurrent Write',
        operations: 10000,
        concurrent: 100,
        action: 'write'
      },
      {
        name: 'Random Read',
        operations: 100000,
        concurrent: 50,
        action: 'read'
      },
      {
        name: 'Search Performance',
        operations: 1000,
        concurrent: 10,
        action: 'search'
      },
      {
        name: 'Mixed Workload',
        operations: 50000,
        concurrent: 50,
        action: 'mixed'
      }
    ];
  }

  // 시나리오 실행
  async runScenario(scenario, vaultPath) {
    const startTime = performance.now();
    const operations = [];

    // 작업 생성
    for (let i = 0; i < scenario.operations; i++) {
      operations.push(this.createOperation(scenario.action, i));
    }

    // 동시 실행
    const batches = this.createBatches(operations, scenario.concurrent);
    const results = [];

    for (const batch of batches) {
      const batchResults = await Promise.all(
        batch.map(op => this.executeOperation(op, vaultPath))
      );
      results.push(...batchResults);
    }

    const endTime = performance.now();

    // 결과 분석
    return {
      scenario: scenario.name,
      totalTime: endTime - startTime,
      operations: scenario.operations,
      throughput: scenario.operations / ((endTime - startTime) / 1000),
      latency: this.calculateLatency(results),
      errors: results.filter(r => r.error).length
    };
  }

  // 보고서 생성
  generateReport() {
    const report = {
      timestamp: new Date(),
      results: Array.from(this.results.values()),
      summary: {
        totalOperations: 0,
        averageThroughput: 0,
        p99Latency: 0,
        errorRate: 0
      }
    };

    // 요약 계산
    let totalThroughput = 0;
    let totalErrors = 0;
    let allLatencies = [];

    for (const result of report.results) {
      report.summary.totalOperations += result.operations;
      totalThroughput += result.throughput;
      totalErrors += result.errors;
      allLatencies.push(...result.latency.raw);
    }

    report.summary.averageThroughput = totalThroughput / report.results.length;
    report.summary.errorRate = totalErrors / report.summary.totalOperations;
    report.summary.p99Latency = this.percentile(allLatencies, 99);

    return report;
  }

  createBatches(items, batchSize) {
    const batches = [];
    for (let i = 0; i < items.length; i += batchSize) {
      batches.push(items.slice(i, i + batchSize));
    }
    return batches;
  }

  calculateLatency(results) {
    const latencies = results.map(r => r.duration);
    
    return {
      min: Math.min(...latencies),
      max: Math.max(...latencies),
      avg: latencies.reduce((a, b) => a + b, 0) / latencies.length,
      p50: this.percentile(latencies, 50),
      p95: this.percentile(latencies, 95),
      p99: this.percentile(latencies, 99),
      raw: latencies
    };
  }

  percentile(arr, p) {
    const sorted = arr.sort((a, b) => a - b);
    const index = Math.ceil((p / 100) * sorted.length) - 1;
    return sorted[index];
  }
}
```

## 마무리

이번 강의에서는 대규모 볼트 관리의 모든 측면을 다루었습니다. 수천, 수만 개의 노트를 효율적으로 관리하기 위한 아키텍처 설계, 성능 최적화, 백업 전략, 그리고 대규모 팀 협업 방법을 학습했습니다.

### 핵심 요약
1. 확장 가능한 볼트 아키텍처 설계
2. 고성능 인덱싱과 검색 최적화
3. 체계적인 백업과 재해 복구 전략
4. 대규모 팀을 위한 협업 인프라
5. 지속적인 모니터링과 최적화

### 다음 강의 예고
제31강(최종강)에서는 실전 프로젝트를 통해 지금까지 학습한 모든 내용을 종합하여 적용하는 방법을 다루겠습니다.